from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from family_api.controllers.baby import add_baby
from family_api.schemas import BabySchema


class BabyListView(web.View):

    @docs(summary="Register new family")
    @request_schema(BabySchema())
    @response_schema(BabySchema(), code=201)
    async def post(self):
        schema = BabySchema()
        family_id = int(self.request.match_info['family_id'])
        baby = schema.load(await self.request.json())
        async with self.request.app['db'].acquire() as conn:
            stored_baby = await add_baby(family_id, baby, conn)
        return web.json_response(schema.dump(stored_baby), status=201)
