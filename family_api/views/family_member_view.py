from aiohttp import web
from aiohttp_apispec import request_schema, docs, response_schema

from family_api.controllers.family_member import accept_member_invitation, issue_invitation_token, remove_family_member
from family_api.decorators import is_current_user_in_family
from family_api.schemas import InvitationTokenSchema


class FamilyMemberListView(web.View):
    @docs(summary="Accept member invitation",
          responses={204: "Successfully invited"})
    @request_schema(InvitationTokenSchema())
    async def put(self):
        user_uuid = self.request['token_data']['user_claims']['uuid']
        schema = InvitationTokenSchema()
        family_uuid = self.request.match_info['family_uuid']
        issued_token = schema.load(await self.request.json())
        async with self.request.app['db'].acquire() as conn:
            await accept_member_invitation(family_uuid, issued_token['token'], user_uuid, conn)
        return web.Response(status=204)


class FamilyMemberTokenView(web.View):
    @docs(summary="Issue new invitation token")
    @response_schema(InvitationTokenSchema())
    @is_current_user_in_family
    async def post(self):
        schema = InvitationTokenSchema()
        family_uuid = self.request.match_info['family_uuid']
        async with self.request.app['db'].acquire() as conn:
            token = await issue_invitation_token(family_uuid, conn)
        return web.json_response(schema.dump(token))


class FamilyMemberView(web.View):
    @docs(summary="Remove family member",
          responses={204: "Successfully deleted"})
    @is_current_user_in_family
    async def delete(self):
        family_uuid = self.request.match_info['family_uuid']
        member_uuid = self.request.match_info['member_uuid']
        async with self.request.app['db'].acquire() as conn:
            await remove_family_member(family_uuid, member_uuid, conn)
        return web.Response(status=204)
