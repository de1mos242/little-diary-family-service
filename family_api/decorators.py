from functools import wraps

from aiohttp.web_exceptions import HTTPForbidden

from family_api.repositories.family_member_repository import get_by_family_id_and_user_uuid


def is_current_user_in_family(func, family_id_param_name='family_id'):
    @wraps(func)
    async def wrapper(cls, *args, **kwargs):
        current_user_uuid = cls.request['user_uuid']
        family_id = cls.request.match_info[family_id_param_name]
        async with cls.request.app['db'].acquire() as conn:
            family_member_exist = await get_by_family_id_and_user_uuid(family_id, current_user_uuid, conn)
        if family_member_exist:
            return await func(cls, *args, **kwargs)
        raise HTTPForbidden()

    return wrapper
