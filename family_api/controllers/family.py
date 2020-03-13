from aiohttp.web_exceptions import HTTPNotFound

from family_api.repositories import family_member_repository, baby_repository, family_repository
from family_api.repositories.family_repository import insert_family, get_by_id


async def register_family(family_obj, conn):
    family_id = await insert_family(family_obj, conn)
    stored_family = await get_by_id(family_id, conn)
    return stored_family


async def get_family_info(family_id: int, conn):
    family = await get_by_id(family_id, conn)
    if not family:
        raise HTTPNotFound()
    family = dict(family)
    family['members'] = await family_member_repository.find_by_family_id(family_id, conn)
    family['babies'] = await baby_repository.find_by_family_id(family_id, conn)
    return family


async def update_family(family_id: int, family_data, conn):
    return await family_repository.update_family(family_id, family_data, conn)
