import json
from uuid import uuid4

from aiohttp import web
from aiohttp.test_utils import TestClient

from family_api.repositories import baby_repository


async def test_create_baby(app: web.Application, cli: TestClient, make_headers,
                           default_family_with_member):
    baby_uuid = uuid4()
    user_uuid, family, _ = default_family_with_member
    data = {"first_name": "Adam",
            "date_of_birth": "2018-01-01"}

    resp = await cli.put(f"/v1/family/{family['family_uuid']}/baby/{baby_uuid}",
                         data=json.dumps(data),
                         headers=make_headers(user_uuid))
    assert resp.status == 201, await resp.text()
    response = await resp.json()

    assert response['first_name'] == data['first_name']
    assert response['date_of_birth'] == data['date_of_birth']

    async with app['db'].acquire() as conn:
        babies = await baby_repository.find_by_family_id(family['id'], conn)
    assert len(babies) == 1
    assert babies[0]['first_name'] == data['first_name']
    assert babies[0]['date_of_birth'].strftime("%Y-%m-%d") == data['date_of_birth']

    assert response['uuid'] == babies[0]['baby_uuid']
    assert response['uuid'] == str(baby_uuid)


async def test_update_baby(app: web.Application, cli: TestClient, make_headers, baby_factory,
                           default_family_with_member):
    user_uuid, family, _ = default_family_with_member
    async with app['db'].acquire() as conn:
        baby = baby_factory.create(family_id=family['id'])
        baby['id'] = await baby_repository.insert_baby(baby, conn)

    data = {"first_name": "Adam",
            "date_of_birth": "2018-01-01"}

    resp = await cli.put(f"/v1/family/{family['family_uuid']}/baby/{baby['baby_uuid']}",
                         data=json.dumps(data),
                         headers=make_headers(user_uuid))
    assert resp.status == 200, await resp.text()
    response = await resp.json()

    assert response['first_name'] == data['first_name']
    assert response['date_of_birth'] == data['date_of_birth']

    async with app['db'].acquire() as conn:
        babies = await baby_repository.find_by_family_id(family['id'], conn)
    assert len(babies) == 1
    assert babies[0]['id'] == baby['id']
    assert babies[0]['baby_uuid'] == baby['baby_uuid']
    assert babies[0]['first_name'] == data['first_name']
    assert babies[0]['date_of_birth'].strftime("%Y-%m-%d") == data['date_of_birth']


async def test_delete_baby(app: web.Application, cli: TestClient, make_headers, baby_factory,
                           default_family_with_member):
    user_uuid, family, _ = default_family_with_member
    async with app['db'].acquire() as conn:
        baby = baby_factory.create(family_id=family['id'])
        baby['id'] = await baby_repository.insert_baby(baby, conn)

    resp = await cli.delete(f"/v1/family/{family['family_uuid']}/baby/{baby['baby_uuid']}",
                            headers=make_headers(user_uuid))
    assert resp.status == 204, await resp.text()
    async with app['db'].acquire() as conn:
        babies = await baby_repository.find_by_family_id(family['id'], conn)
    assert len(babies) == 0
