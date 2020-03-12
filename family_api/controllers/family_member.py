from uuid import UUID

from family_api.repositories.family_member_repository import insert_family_member


async def add_family_member(family_obj, user_uuid: UUID, conn):
    family_member_obj = dict(family_id=family_obj.id, user_uuid=str(user_uuid))
    await insert_family_member(family_member_obj, conn)
