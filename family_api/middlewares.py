import re
from typing import List
from uuid import UUID

from aiohttp.web_exceptions import HTTPUnauthorized
from aiohttp.web_middlewares import middleware


def get_current_user_middleware(whitelist: List[str]):
    @middleware
    async def current_user_middleware(request, handler):
        if not check_request(request, whitelist):
            claims = request.get('token_data', {}).get('user_claims', {})
            user_uuid = claims.get('uuid')
            user_role = claims.get('role')
            if not user_uuid or not user_role:
                raise HTTPUnauthorized(text="JWT token is invalid")
            request['user_uuid'] = UUID(user_uuid)
            request['user_role'] = user_role
        return await handler(request)

    return current_user_middleware


def check_request(request, entries):
    for pattern in entries:
        if re.match(pattern, request.path):
            return True

    return False
