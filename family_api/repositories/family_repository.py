from family_api.models import families_table


async def insert_family(family_obj, conn) -> int:
    return await conn.scalar(families_table.insert().values(family_obj))


async def update_family(family_id, family_obj, conn):
    return await conn.execute(families_table.update().values(family_obj).where(families_table.c.id == family_id))


async def delete_family(family_id, conn):
    return await conn.execute(families_table.delete().where(families_table.c.id == family_id))


async def get_by_id(family_id, conn):
    return await (await conn.execute(families_table.select().where(families_table.c.id == family_id))).first()
