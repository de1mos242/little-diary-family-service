from uuid import UUID, uuid4

from aiohttp.web_exceptions import HTTPNotFound

from family_api.repositories import family_member_repository, baby_repository, family_repository
from family_api.repositories.family_repository import insert_family, get_by_id, get_by_uuid


async def register_family(family_obj, conn):
    family_id = await insert_family(family_obj, conn)
    stored_family = await get_by_id(family_id, conn)
    return stored_family


async def get_family_info(family_uuid: int, conn):
    family = await get_by_uuid(family_uuid, conn)
    if not family:
        raise HTTPNotFound()
    family = dict(family)
    family['members'] = await family_member_repository.find_by_family_id(family['id'], conn)
    family['babies'] = await baby_repository.find_by_family_id(family['id'], conn)
    return family


async def create_or_update_family(family_uuid: UUID, family_data: dict, user_uuid: UUID, conn):
    family = await family_repository.get_by_uuid(family_uuid, conn)
    if family:
        await family_repository.update_family(family.id, family_data, conn)
        created = False
    else:
        family_data['family_uuid'] = family_uuid
        family_id = await family_repository.insert_family(family_data, conn)
        family_member_obj = dict(family_id=family_id, user_uuid=str(user_uuid), member_uuid=str(uuid4()))
        await family_member_repository.insert_family_member(family_member_obj, conn)
        created = True
    return await family_repository.get_by_uuid(family_uuid, conn), created


async def update_family(family_id: int, family_data, conn):
    return await family_repository.update_family(family_id, family_data, conn)


async def delete_family(family_uuid: int, conn):
    family = await get_by_uuid(family_uuid, conn)
    if not family:
        raise HTTPNotFound()
    return await family_repository.delete_family(family.id, conn)
