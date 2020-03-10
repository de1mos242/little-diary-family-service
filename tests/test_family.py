import json
from uuid import uuid4

from family_api.models import family


async def test_create_family(app, cli, make_headers):
    user_uuid = uuid4()
    resp = await cli.post("/v1/family", data=json.dumps({'title': "My super family"}), headers=make_headers(user_uuid))
    assert resp.status == 200, await resp.text()

    response = await resp.json()
    assert response['title'] == "My super family"
    assert response['id'] > 0

    async with app['db'].acquire() as conn:
        stored_family = await (await conn.execute(family.select().where(family.c.id == response['id']))).first()
    assert stored_family is not None
    assert stored_family.id == response['id']
    assert stored_family.title == "My super family"
