from uuid import uuid4

from aiohttp import web
from aiohttp.test_utils import TestClient

from family_api.repositories import baby_repository


async def test_user_has_access_to_baby(app: web.Application, cli: TestClient, make_headers, make_tech_headers,
                                       default_family_with_member, baby_factory):
    user_uuid, family, _ = default_family_with_member
    async with app['db'].acquire() as conn:
        baby = baby_factory.create(family_id=family['id'])
        baby['id'] = await baby_repository.insert_baby(baby, conn)

    resp = await cli.get(f"/v1/access/{user_uuid}/baby/{baby['baby_uuid']}", headers=make_headers(uuid4()))
    assert resp.status == 403, await resp.text()

    resp = await cli.get(f"/v1/access/{uuid4()}/baby/{baby['baby_uuid']}", headers=make_tech_headers(uuid4()))
    assert resp.status == 200, await resp.text()

    response = await resp.json()
    assert response["has_access"] is False

    resp = await cli.get(f"/v1/access/{user_uuid}/baby/{baby['baby_uuid']}", headers=make_tech_headers(uuid4()))
    assert resp.status == 200, await resp.text()

    response = await resp.json()
    assert response["has_access"] is True
