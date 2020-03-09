from uuid import UUID

from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from marshmallow import Schema, fields

from family_api.controllers.family import register_family
from family_api.controllers.family_member import add_family_member


class FamilySchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, allow_none=False)


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
