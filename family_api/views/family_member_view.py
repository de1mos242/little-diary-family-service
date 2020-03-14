from aiohttp import web
from aiohttp_apispec import request_schema, docs, response_schema

from family_api.controllers.family_member import accept_member_invitation, issue_invitation_token
from family_api.schemas import TokenSchema


class FamilyMemberListView(web.View):
    @docs(summary="Accept member invitation",
          responses={204: "Successfully invited"})
    @request_schema(TokenSchema())
    async def post(self):
        user_uuid = self.request['token_data']['user_claims']['uuid']
        schema = TokenSchema()
        family_id = int(self.request.match_info['family_id'])
        issued_token = schema.load(await self.request.json())
        async with self.request.app['db'].acquire() as conn:
            await accept_member_invitation(family_id, issued_token['token'], user_uuid, conn)
        return web.Response(status=204)


class FamilyMemberTokenView(web.View):
    @docs(summary="Issue new invitation token")
    @response_schema(TokenSchema())
    async def post(self):
        schema = TokenSchema()
        family_id = int(self.request.match_info['family_id'])
        async with self.request.app['db'].acquire() as conn:
            token = await issue_invitation_token(family_id, conn)
        return web.json_response(schema.dump(token))
