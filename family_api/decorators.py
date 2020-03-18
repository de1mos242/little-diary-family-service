from functools import wraps

from aiohttp.web_exceptions import HTTPForbidden

from family_api.repositories import family_repository
from family_api.repositories.family_member_repository import get_by_family_id_and_user_uuid


def is_current_user_in_family_or_new(func, family_uuid_param_name='family_uuid'):
    @wraps(func)
    async def wrapper(cls, *args, **kwargs):
        current_user_uuid = cls.request['user_uuid']
        family_uuid = cls.request.match_info[family_uuid_param_name]
        async with cls.request.app['db'].acquire() as conn:
            family = await family_repository.get_by_uuid(family_uuid, conn)
            if family:
                family_member_exist = await get_by_family_id_and_user_uuid(family.id, current_user_uuid, conn)
        if family and not family_member_exist:
            raise HTTPForbidden()
        return await func(cls, *args, **kwargs)

    return wrapper
