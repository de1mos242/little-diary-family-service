from aiohttp.web_exceptions import HTTPNotFound

from family_api.repositories import baby_repository, family_member_repository


async def check_has_baby_access(user_uuid: str, baby_uuid: str, conn) -> bool:
    baby = await baby_repository.get_by_uuid(baby_uuid, conn)
    if not baby:
        raise HTTPNotFound(text="baby not found")
    family_member = await family_member_repository.get_by_family_id_and_user_uuid(baby['family_id'], user_uuid, conn)
    return family_member is not None
