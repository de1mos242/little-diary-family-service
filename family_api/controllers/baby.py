from uuid import uuid4

from aiohttp.web_exceptions import HTTPNotFound, HTTPBadRequest

from family_api.repositories.baby_repository import insert_baby, get_by_id, get_by_uuid, update_baby, delete_baby


async def add_baby(family_id: int, baby_input: dict, conn) -> dict:
    baby_input['family_id'] = family_id
    baby_input['baby_uuid'] = str(uuid4())
    baby_id = await insert_baby(baby_input, conn)
    return await get_by_id(baby_id, conn)


async def update_baby_fields(family_id: int, baby_uuid: str, baby_input: dict, conn) -> dict:
    baby = await get_by_uuid(baby_uuid, conn)
    if not baby:
        raise HTTPNotFound(text="Baby not found")
    if baby['family_id'] != family_id:
        raise HTTPBadRequest(text="Baby and family mismatch")
    await update_baby(baby['id'], baby_input, conn)
    return await get_by_id(baby['id'], conn)


async def remove_baby(family_id: int, baby_uuid: str, conn):
    baby = await get_by_uuid(baby_uuid, conn)
    if not baby:
        raise HTTPNotFound(text="Baby not found")
    if baby['family_id'] != family_id:
        raise HTTPBadRequest(text="Baby and family mismatch")
    await delete_baby(baby['id'], conn)
