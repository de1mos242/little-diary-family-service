from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from family_api.controllers.family import get_family_info, delete_family, \
    create_or_update_family
from family_api.decorators import is_current_user_in_family_or_new, is_current_user_in_family
from family_api.schemas import FamilySchema


class FamilyView(web.View):

    @docs(summary="Get family info")
    @response_schema(FamilySchema())
    @is_current_user_in_family
    async def get(self):
        schema = FamilySchema()
        family_uuid = self.request.match_info['family_uuid']
        async with self.request.app['db'].acquire() as conn:
            family = await get_family_info(family_uuid, conn)
        return web.json_response(schema.dump(family))

    @docs(summary="Update family info",
          responses={200: "Successfully updated",
                     201: "Successfully created"})
    @request_schema(FamilySchema())
    @is_current_user_in_family_or_new
    async def put(self):
        user_uuid = self.request['token_data']['user_claims']['uuid']
        schema = FamilySchema()
        family_uuid = self.request.match_info['family_uuid']
        family_obj = schema.load(await self.request.json())
        async with self.request.app['db'].acquire() as conn:
            stored_family, created = await create_or_update_family(family_uuid, family_obj, user_uuid, conn)
        return web.json_response(schema.dump(stored_family), status=201 if created else 200)

    @docs(summary="Delete family",
          responses={204: "Successfully deleted"})
    @is_current_user_in_family
    async def delete(self):
        family_uuid = self.request.match_info['family_uuid']
        async with self.request.app['db'].acquire() as conn:
            await delete_family(family_uuid, conn)
        return web.Response(status=204)
