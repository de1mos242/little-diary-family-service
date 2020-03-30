import sqlalchemy as sa

from family_api.models import families_table, family_members_table


async def insert_family(family_obj, conn) -> int:
    return await conn.scalar(families_table.insert().values(family_obj))


async def update_family(family_id, family_obj, conn):
    return await conn.execute(families_table.update().values(family_obj).where(families_table.c.id == family_id))


async def delete_family(family_id, conn):
    return await conn.execute(families_table.delete().where(families_table.c.id == family_id))


async def get_by_id(family_id, conn):
    return await (await conn.execute(families_table.select().where(families_table.c.id == family_id))).first()


async def get_by_uuid(family_uuid, conn):
    query = families_table.select().where(families_table.c.family_uuid == family_uuid)
    return await (await conn.execute(query)).first()


async def get_by_family_member(user_uuid, conn):
    subquery = (sa.select([family_members_table.c.family_id])).select_from(family_members_table)
    subquery = subquery.where(family_members_table.c.user_uuid == user_uuid).alias('member')
    query = families_table.select().where(families_table.c.id.in_(subquery))
    return [row async for row in conn.execute(query)]
