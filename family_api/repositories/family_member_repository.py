from family_api.models import family_members_table


async def insert_family_member(family_member_obj, conn) -> int:
    return await conn.scalar(family_members_table.insert().values(family_member_obj))
