import json

from aiohttp import web
from aiohttp.test_utils import TestClient

from family_api.repositories import baby_repository


async def test_delete_family_member(app: web.Application, cli: TestClient, make_headers,
                                    add_default_family_with_member):
    user_uuid, family, _ = add_default_family_with_member
    data = {"first_name": "Adam",
            "date_of_birth": "2018-01-01"}

    resp = await cli.post(f"/v1/family/{family['id']}/baby",
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
