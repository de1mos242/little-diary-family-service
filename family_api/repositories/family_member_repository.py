from typing import List
from uuid import UUID

from family_api.models import family_members_table


async def insert_family_member(family_member_obj, conn) -> int:
    return await conn.scalar(family_members_table.insert().values(family_member_obj))


async def get_by_family_id_and_user_uuid(family_id: int, user_uuid: UUID, conn) -> dict:
    query = family_members_table.select()
    query = query.where(family_members_table.c.family_id == family_id)
    query = query.where(family_members_table.c.user_uuid == str(user_uuid))
    return await (await conn.execute(query)).first()


async def find_by_family_id(family_id, conn) -> List[dict]:
    select_query = family_members_table.select().where(family_members_table.c.family_id == family_id)
    return [row async for row in conn.execute(select_query)]


async def get_by_id(member_id: int, conn) -> dict:
    query = family_members_table.select().where(family_members_table.c.id == member_id)
    return await (await conn.execute(query)).first()


async def get_by_uuid(member_uuid: str, conn) -> dict:
    query = family_members_table.select().where(family_members_table.c.member_uuid == member_uuid)
    return await (await conn.execute(query)).first()


async def delete(member_id: int, conn):
    await conn.execute(family_members_table.delete().where(family_members_table.c.id == member_id))
