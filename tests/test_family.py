import json
from uuid import uuid4

from aiohttp import web
from aiohttp.test_utils import TestClient

from family_api.models import families_table
from family_api.repositories import family_repository, family_member_repository, baby_repository


async def test_create_family(app: web.Application, cli: TestClient, make_headers):
    user_uuid = uuid4()
    resp = await cli.post("/v1/family", data=json.dumps({'title': "My super family"}), headers=make_headers(user_uuid))
    assert resp.status == 200, await resp.text()

    response = await resp.json()
    assert response['title'] == "My super family"
    assert response['id'] > 0

    async with app['db'].acquire() as conn:
        stored_family = await (
            await conn.execute(families_table.select().where(families_table.c.id == response['id']))).first()
    assert stored_family is not None
    assert stored_family.id == response['id']
    assert stored_family.title == "My super family"


async def test_get_family_info(app: web.Application, cli: TestClient, make_headers, family_factory,
                               family_member_factory, baby_factory):
    user_uuid = str(uuid4())
    async with app['db'].acquire() as conn:
        family = family_factory.create()
        family['id'] = await family_repository.insert_family(family, conn)
        family_member = family_member_factory.create(family_id=family['id'], user_uuid=user_uuid)
        family_member['id'] = await family_member_repository.insert_family_member(family_member, conn)
        baby = baby_factory.create(family_id=family['id'])
        baby['id'] = await baby_repository.insert_baby(baby, conn)

    resp = await cli.get(f"/v1/family/{family['id']}", headers=make_headers(user_uuid))
    assert resp.status == 200, await resp.text()

    response = await resp.json()
    assert response['id'] == family['id']
    assert response['title'] == family['title']

    assert len(response['members']) == 1
    assert response['members'][0]['id'] == family_member['id']
    assert response['members'][0]['user_uuid'] == family_member['user_uuid']

    assert len(response['babies']) == 1
    assert response['babies'][0]['uuid'] == baby['baby_uuid']
    assert response['babies'][0]['first_name'] == baby['first_name']
    assert response['babies'][0]['date_of_birth'] == baby['date_of_birth'].strftime("%Y-%m-%dT%H:%M:%S.%f")
