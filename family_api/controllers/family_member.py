from datetime import datetime
from uuid import UUID

from aiohttp.web_exceptions import HTTPNotFound, HTTPForbidden, HTTPBadRequest

from family_api.enums import TokenType
from family_api.repositories import family_repository, issued_token_repository, family_member_repository
from family_api.repositories.family_member_repository import insert_family_member


async def add_family_member(family_obj, user_uuid: UUID, conn):
    family_member_obj = dict(family_id=family_obj.id, user_uuid=str(user_uuid))
    await insert_family_member(family_member_obj, conn)


async def accept_member_invitation(family_id, token, user_uuid: UUID, conn):
    family = await family_repository.get_by_id(family_id, conn)
    issued_token = await issued_token_repository.get_token(token, conn)
    if not family:
        raise HTTPNotFound(text=f"Family with id {family_id} not found")
    if not issued_token or issued_token.expired_at < datetime.now():
        raise HTTPForbidden(text="Token not found or expired")
    if issued_token.token_type != TokenType.MEMBER_INVITATION:
        raise HTTPBadRequest(text="Token invalid")

    family_member_obj = dict(family_id=family_id, user_uuid=str(user_uuid))
    await family_member_repository.insert_family_member(family_member_obj, conn)
    await issued_token_repository.delete_issued_token(issued_token.id, conn)
