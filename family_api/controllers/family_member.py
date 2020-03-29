from datetime import datetime, timedelta
from uuid import UUID, uuid4

from aiohttp.web_exceptions import HTTPNotFound, HTTPForbidden, HTTPBadRequest

from family_api.config import Config
from family_api.enums import TokenType
from family_api.repositories import family_repository, issued_token_repository, family_member_repository


async def accept_member_invitation(family_uuid, token, user_uuid: UUID, conn):
    family = await family_repository.get_by_uuid(family_uuid, conn)
    issued_token = await issued_token_repository.get_token(token, conn)
    if not family:
        raise HTTPNotFound(text=f"Family with uuid {family_uuid} not found")
    if not issued_token or issued_token.expired_at < datetime.now():
        raise HTTPForbidden(text="Token not found or expired")
    if issued_token.token_type != TokenType.MEMBER_INVITATION or issued_token.related_entity_id != family.id:
        raise HTTPBadRequest(text="Token invalid")

    family_member_obj = dict(family_id=family.id, user_uuid=str(user_uuid), member_uuid=str(uuid4()))
    await family_member_repository.insert_family_member(family_member_obj, conn)
    await issued_token_repository.delete_issued_token(issued_token.id, conn)


async def issue_invitation_token(family_uuid, conn):
    family = await family_repository.get_by_uuid(family_uuid, conn)
    if not family:
        raise HTTPNotFound(text=f"Family with uuid {family_uuid} not found")
    issued_token = dict(token=uuid4(),
                        expired_at=datetime.now() + timedelta(seconds=Config.INVITATION_TOKEN_EXPIRE_SECONDS),
                        token_type=TokenType.MEMBER_INVITATION,
                        related_entity_id=family.id)
    token_id = await issued_token_repository.insert_token(issued_token, conn)
    return await issued_token_repository.get_by_id(token_id, conn)


async def remove_family_member(family_uuid: str, member_uuid: str, conn):
    family = await family_repository.get_by_uuid(family_uuid, conn)
    if not family:
        raise HTTPNotFound(text=f"Family with uuid {family_uuid} not found")
    member = await family_member_repository.get_by_uuid(member_uuid, conn)
    if not member:
        raise HTTPNotFound(text="Family member not found")
    if member['family_id'] != family.id:
        raise HTTPBadRequest(text="Member and family mismatch")
    await family_member_repository.delete(member['id'], conn)
