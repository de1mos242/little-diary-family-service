from uuid import UUID

from family_api.models import family, family_member


async def add_family_member(family_obj: family, user_uuid: UUID, conn):
    family_member_obj = dict(family_id=family_obj.id, user_uuid=str(user_uuid))
    await conn.execute(family_member.insert().values(family_member_obj))
