from aiohttp.test_utils import TestClient


async def test_get_health_check(cli: TestClient):
    resp = await cli.get(f"/status/health")
    assert resp.status == 200, await resp.text()
