from typing import List

from family_api.models import babies_table


async def insert_baby(baby, conn) -> int:
    return await conn.scalar(babies_table.insert().values(baby))


async def get_by_id(baby_id, conn) -> dict:
    return await(await conn.execute(babies_table.select().where(babies_table.c.id == baby_id))).first()


async def find_by_family_id(family_id, conn) -> List[dict]:
    select_query = babies_table.select().where(babies_table.c.family_id == family_id)
    return [row async for row in conn.execute(select_query)]
