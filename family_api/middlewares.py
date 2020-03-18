from uuid import UUID

from aiohttp.web_exceptions import HTTPUnauthorized
from aiohttp.web_middlewares import middleware


@middleware
async def current_user_middleware(request, handler):
    claims = request.get('token_data', {}).get('user_claims', {})
    user_uuid = claims.get('uuid')
    user_role = claims.get('role')
    user_resources = claims.get('resources', [])
    if not user_uuid or not user_role:
        raise HTTPUnauthorized(text="JWT token is invalid")
    request['user_uuid'] = UUID(user_uuid)
    request['user_role'] = user_role
    request['user_resources'] = user_resources
    return await handler(request)
