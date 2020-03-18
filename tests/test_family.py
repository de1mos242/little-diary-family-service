import json
from uuid import uuid4

from aiohttp import web
from aiohttp.test_utils import TestClient

from family_api.repositories import family_repository, family_member_repository, baby_repository


async def test_create_family(app: web.Application, cli: TestClient, make_headers):
    user_uuid = uuid4()
    family_uuid = uuid4()
    resp = await cli.put(f"/v1/family/{family_uuid}", data=json.dumps({'title': "My super family"}),
                         headers=make_headers(user_uuid))
    assert resp.status == 201, await resp.text()

    response = await resp.json()
    assert response['title'] == "My super family"
    assert response['uuid'] == str(family_uuid)

    async with app['db'].acquire() as conn:
        stored_family = await family_repository.get_by_uuid(str(family_uuid), conn)
    assert stored_family is not None
    assert stored_family.title == "My super family"


# pylint: disable=too-many-arguments
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

        another_family = family_factory.create()
        await family_repository.insert_family(another_family, conn)

    resp = await cli.get(f"/v1/family/{another_family['family_uuid']}", headers=make_headers(user_uuid))
    assert resp.status == 403, await resp.text()
    resp = await cli.get(f"/v1/family/{uuid4()}", headers=make_headers(user_uuid))
    assert resp.status == 404, await resp.text()

    resp = await cli.get(f"/v1/family/{family['family_uuid']}", headers=make_headers(user_uuid))
    assert resp.status == 200, await resp.text()

    response = await resp.json()
    assert response['uuid'] == family['family_uuid']
    assert response['title'] == family['title']

    assert len(response['members']) == 1
    assert response['members'][0]['uuid'] == family_member['member_uuid']
    assert response['members'][0]['user_uuid'] == family_member['user_uuid']

    assert len(response['babies']) == 1
    assert response['babies'][0]['uuid'] == baby['baby_uuid']
    assert response['babies'][0]['first_name'] == baby['first_name']
    assert response['babies'][0]['date_of_birth'] == baby['date_of_birth'].strftime("%Y-%m-%d")


async def test_update_family(app: web.Application, cli: TestClient, make_headers, family_factory,
                             family_member_factory):
    user_uuid = str(uuid4())
    async with app['db'].acquire() as conn:
        family = family_factory.create()
        family['id'] = await family_repository.insert_family(family, conn)
        family_member = family_member_factory.create(family_id=family['id'], user_uuid=user_uuid)
        family_member['id'] = await family_member_repository.insert_family_member(family_member, conn)
        another_family = family_factory.create()
        another_family['id'] = await family_repository.insert_family(another_family, conn)

    resp = await cli.put(f"/v1/family/{another_family['family_uuid']}",
                         data=json.dumps({'title': "My super family"}),
                         headers=make_headers(user_uuid))
    assert resp.status == 403, await resp.text()

    resp = await cli.put(f"/v1/family/{family['family_uuid']}",
                         data=json.dumps({'title': "My super family"}),
                         headers=make_headers(user_uuid))
    assert resp.status == 200, await resp.text()

    async with app['db'].acquire() as conn:
        stored_family = await family_repository.get_by_id(family['id'], conn)
    assert stored_family is not None
    assert stored_family.family_uuid == family['family_uuid']
    assert stored_family.title == "My super family"


async def test_delete_family(app: web.Application, cli: TestClient, make_headers, family_factory,
                             family_member_factory):
    user_uuid = str(uuid4())
    async with app['db'].acquire() as conn:
        family = family_factory.create()
        family['id'] = await family_repository.insert_family(family, conn)
        another_family = family_factory.create()
        another_family['id'] = await family_repository.insert_family(another_family, conn)
        family_member = family_member_factory.create(family_id=family['id'], user_uuid=user_uuid)
        family_member['id'] = await family_member_repository.insert_family_member(family_member, conn)

    resp = await cli.delete(f"/v1/family/{another_family['family_uuid']}",
                            headers=make_headers(user_uuid))
    assert resp.status == 403, await resp.text()

    resp = await cli.delete(f"/v1/family/{family['family_uuid']}",
                            headers=make_headers(user_uuid))
    assert resp.status == 204, await resp.text()

    async with app['db'].acquire() as conn:
        stored_family = await family_repository.get_by_id(family['id'], conn)
    assert stored_family is None
