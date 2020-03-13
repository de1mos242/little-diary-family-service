from aiohttp import web
from aiohttp_apispec import request_schema, docs

from family_api.controllers.family_member import accept_member_invitation
from family_api.schemas import IssuedTokenSchema


class FamilyMemberListView(web.View):
    @docs(summary="Accept member invitation",
          responses={204: "Successfully invited"})
    @request_schema(IssuedTokenSchema())
    async def post(self):
        user_uuid = self.request['token_data']['user_claims']['uuid']
        schema = IssuedTokenSchema()
        family_id = self.request.match_info['family_id']
        issued_token = schema.load(await self.request.json())
        async with self.request.app['db'].acquire() as conn:
            await accept_member_invitation(family_id, issued_token['token'], user_uuid, conn)
        return web.Response(status=204)
