from typing import Tuple

from aiohttp.web_exceptions import HTTPNotFound, HTTPBadRequest

from family_api.repositories import family_repository
from family_api.repositories.baby_repository import insert_baby, get_by_id, get_by_uuid, update_baby, delete_baby


async def create_or_update_baby_fields(family_uuid: str, baby_uuid: str, baby_input: dict, conn) -> Tuple[dict, bool]:
    family = await get_family(family_uuid, conn)
    baby = await get_by_uuid(baby_uuid, conn)

    if not baby:
        baby_input['family_id'] = family.id
        baby_input['baby_uuid'] = baby_uuid
        baby_id = await insert_baby(baby_input, conn)
        created = True
    else:
        baby_id = baby['id']
        if baby['family_id'] != family.id:
            raise HTTPBadRequest(text="Baby and family mismatch")
        await update_baby(baby_id, baby_input, conn)
        created = False

    return await get_by_id(baby_id, conn), created


async def remove_baby(family_uuid: str, baby_uuid: str, conn):
    family = await get_family(family_uuid, conn)
    baby = await get_by_uuid(baby_uuid, conn)
    if not baby:
        raise HTTPNotFound(text="Baby not found")
    if baby['family_id'] != family.id:
        raise HTTPBadRequest(text="Baby and family mismatch")
    await delete_baby(baby['id'], conn)


async def get_family(family_uuid, conn):
    family = await family_repository.get_by_uuid(family_uuid, conn)
    if not family:
        raise HTTPNotFound(text=f"Family with uuid {family_uuid} not found")
    return family
