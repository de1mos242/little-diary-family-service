from uuid import uuid4

from family_api.repositories.baby_repository import insert_baby, get_by_id


async def add_baby(family_id: int, baby_input: dict, conn) -> dict:
    baby_input['family_id'] = family_id
    baby_input['baby_uuid'] = str(uuid4())
    baby_id = await insert_baby(baby_input, conn)
    return await get_by_id(baby_id, conn)
