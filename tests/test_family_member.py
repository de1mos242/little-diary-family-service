import json
from datetime import datetime
from uuid import uuid4

from aiohttp import web
from aiohttp.test_utils import TestClient

from family_api.enums import TokenType
from family_api.repositories import family_repository, issued_token_repository, family_member_repository


async def test_accept_invitation(app: web.Application, cli: TestClient, make_headers, family_factory,
                                 issued_token_factory):
    user_uuid = str(uuid4())
    async with app['db'].acquire() as conn:
        family = family_factory.create()
        family['id'] = await family_repository.insert_family(family, conn)
        issued_token = issued_token_factory.create(related_entity_id=family['id'])
        issued_token['id'] = await issued_token_repository.insert_token(issued_token, conn)

    resp = await cli.post(f"/v1/family/{family['id']}/member",
                          data=json.dumps({'token': issued_token['token']}),
                          headers=make_headers(user_uuid))
    assert resp.status == 204, await resp.text()

    async with app['db'].acquire() as conn:
        family_members = await family_member_repository.find_by_family_id(family['id'], conn)
        issued_token = await issued_token_repository.get_token(issued_token['token'], conn)

    assert len(family_members) == 1
    assert issued_token is None

    assert family_members[0]['user_uuid'] == user_uuid


async def test_create_invitation_token(app: web.Application, cli: TestClient, make_headers, family_factory,
                                       family_member_factory):
    user_uuid = str(uuid4())
    async with app['db'].acquire() as conn:
        family = family_factory.create()
        family['id'] = await family_repository.insert_family(family, conn)
        family_member = family_member_factory.create(family_id=family['id'], user_uuid=user_uuid)
        family_member['id'] = await family_member_repository.insert_family_member(family_member, conn)

    resp = await cli.post(f"/v1/family/{family['id']}/member/token",
                          headers=make_headers(user_uuid))
    assert resp.status == 200, await resp.text()
    response = await resp.json()

    assert response['token'] is not None

    async with app['db'].acquire() as conn:
        issued_token = await issued_token_repository.get_token(response['token'], conn)

    assert issued_token is not None
    assert issued_token['expired_at'] > datetime.now()
    assert issued_token['token_type'] == TokenType.MEMBER_INVITATION
