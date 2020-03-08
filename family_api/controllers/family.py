from family_api.models import family


async def register_family(family_obj, conn):
    family_id = await conn.scalar(family.insert().values(family_obj))
    stored_family = await (await conn.execute(family.select().where(family.c.id == family_id))).first()
    return stored_family
