from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from family_api.controllers.baby import create_or_update_baby_fields, remove_baby
from family_api.decorators import is_current_user_in_family
from family_api.schemas import BabySchema


class BabyView(web.View):
    @docs(summary="Create of update baby info")
    @request_schema(BabySchema())
    @response_schema(BabySchema())
    @is_current_user_in_family
    async def put(self):
        schema = BabySchema()
        family_uuid = self.request.match_info['family_uuid']
        baby_uuid = self.request.match_info['baby_uuid']
        baby = schema.load(await self.request.json())
        async with self.request.app['db'].acquire() as conn:
            stored_baby, created = await create_or_update_baby_fields(family_uuid, baby_uuid, baby, conn)
        return web.json_response(schema.dump(stored_baby), status=201 if created else 200)

    @docs(summary="Delete baby",
          responses={204: "Successfully deleted"})
    @is_current_user_in_family
    async def delete(self):
        family_uuid = self.request.match_info['family_uuid']
        baby_uuid = self.request.match_info['baby_uuid']
        async with self.request.app['db'].acquire() as conn:
            await remove_baby(family_uuid, baby_uuid, conn)
        return web.Response(status=204)
