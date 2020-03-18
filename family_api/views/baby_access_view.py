from aiohttp import web
from aiohttp_apispec import docs, response_schema

from family_api.controllers import access_baby
from family_api.decorators import is_tech_user_has_access
from family_api.schemas import AccessPermissionSchema


class BabyAccessView(web.View):

    @docs(summary="Check user has access to baby")
    @response_schema(AccessPermissionSchema())
    @is_tech_user_has_access
    async def get(self):
        schema = AccessPermissionSchema()
        user_uuid = self.request.match_info['user_uuid']
        baby_uuid = self.request.match_info['baby_uuid']
        async with self.request.app['db'].acquire() as conn:
            has_access = await access_baby.check_has_baby_access(user_uuid, baby_uuid, conn)
        return web.json_response(schema.dump(dict(has_access=has_access)))
