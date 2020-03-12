from family_api.repositories.family_repository import insert_family, get_by_id


async def register_family(family_obj, conn):
    family_id = await insert_family(family_obj, conn)
    stored_family = await get_by_id(family_id, conn)
    return stored_family
