from family_api.models import families_table


async def insert_family(family_obj, conn) -> int:
    return await conn.scalar(families_table.insert().values(family_obj))


async def get_by_id(family_id, conn) -> dict:
    return await (await conn.execute(families_table.select().where(families_table.c.id == family_id))).first()
