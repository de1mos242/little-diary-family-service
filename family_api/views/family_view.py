from uuid import UUID

from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from family_api.controllers.family import register_family, get_family_info, update_family, delete_family
from family_api.controllers.family_member import add_family_member
from family_api.decorators import is_current_user_in_family
from family_api.schemas import FamilySchema


class FamilyListView(web.View):

    @docs(summary="Register new family")
    @request_schema(FamilySchema())
    @response_schema(FamilySchema())
    async def post(self):
        schema = FamilySchema()
        family_obj = schema.load(await self.request.json())
        async with self.request.app['db'].acquire() as conn:
            stored_family = await register_family(family_obj, conn)
            await add_family_member(stored_family, UUID(self.request['token_data']['user_claims']['uuid']), conn)
        return web.json_response(schema.dump(stored_family))


class FamilyView(web.View):

    @docs(summary="Get family info")
    @response_schema(FamilySchema())
    @is_current_user_in_family
    async def get(self):
        schema = FamilySchema()
        family_id = self.request.match_info['family_id']
        async with self.request.app['db'].acquire() as conn:
            family = await get_family_info(family_id, conn)
        return web.json_response(schema.dump(family))

    @docs(summary="Update family info",
          responses={204: "Successfully updated"})
    @request_schema(FamilySchema())
    @is_current_user_in_family
    async def put(self):
        schema = FamilySchema()
        family_id = self.request.match_info['family_id']
        family_obj = schema.load(await self.request.json())
        async with self.request.app['db'].acquire() as conn:
            await update_family(family_id, family_obj, conn)
        return web.Response(status=204)

    @docs(summary="Delete family",
          responses={204: "Successfully deleted"})
    @is_current_user_in_family
    async def delete(self):
        family_id = self.request.match_info['family_id']
        async with self.request.app['db'].acquire() as conn:
            await delete_family(family_id, conn)
        return web.Response(status=204)
