from uuid import UUID, uuid4

import jwt
import pytest
from aiohttp import web
from pytest_factoryboy import register

from family_api import models
from family_api.main import init_app
from family_api.repositories import family_repository, family_member_repository
from tests.factories import FamilyFactory, FamilyMemberFactory, BabyFactory, IssuedTokenFactory

TEST_JWT_PRIVATE_KEY = """
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAro1sbZ6uzi80J5esSkLCmpKt7aG4M7ol39nbscvX0Li3WixX
Y7x8xbv9t3rtWj1gAnVgZHI/BNUw70IPs09yETA/ZG13Ucj2nnYNRDFkX1ahxLjV
17zMZaYQkWdXyXM5qH/X8nmDYARJrOVoSy8hyQqkcNf38qXbnQu7Xtp3isPHVRpU
j7zh1AYPgYTAV8BOpq8lOToi/e5FmKS1ygJ1LmF9lm9LXjk2uLkj5Y7z8jozG86c
8UJ9UA2h9ZRuu4uB09mZL7NXgkWd0XyV7sUDUckQmTGf1cxeoRLZBxz7Og9dGgVj
a1AdzOxEZvrbhzH2piKpGg19rOjVnb8Ssj5NgwIDAQABAoIBAQCkc+exC6zj4wM/
Ph37xRQ1r3YgiZnTWlDuqwHabBPDuRQ958LZ266uWSR8JlvTBjobdty/JggLlJRL
BrFmHbZ5TTyccKnXKwB3YP+0vNg1HpjAj+ghHuZv6lp3s6a4zE+JWhFpiGRnJQMI
2wY8t4YcNGOjUUZwnSTgvDnm7utrluNSb7P9Ko7hXyOo0W8vWN35mxcCbEdd2SrN
w05gC6pow1Kgwb+Xg9ovLP9qmUw73dsz1NU06yjfKOjf34Nvd6PSVK08P3HGhUH4
PziBKdDPJ0mKqkCzN1vKqwdzaMD5NurtZpYJEMoGlLFhDhGXL40xANBBs9ZSHaIB
cj3y7QpRAoGBAOIE2YL+FyTQiBOqTBY/iBqawFKOol8HALW07Cxxkv6Q1ZM77Qiw
bvsJT14xLNJcRdTb/cxmuczjdxMBRvKFGRyMx1GNsPUV/6+i84alZui4/XLwIG2J
7pZpHcnSkCEG8TFzXEh3GbwyUj4xG6m41RELf7hx3z9AJUZoJ3VQmP0rAoGBAMW0
39o1vSe9ASQP4q/jOVzlYeDcRjAgiS7CbnU02oFMUDwuK0Yvc+m0XfMIAtNqMCiX
idRPm7dmlNNA7/LA43IaAWtjlUJpQkJTENUj6zhbimyRG5j0ovlYbh3Exmo9Kx0v
Gyh63ITGC6XbQd9yfTwbDIs92HpT4zj5f3QymrUJAoGBAK5EdP12MpwVGUaoYMAq
viNdPHqrNXC1sotn802VSHR1cedzJiE0AG4Y0JRcsCWGNeWYtci7T/k1TWNe8bge
fa0wsqIj8NQX4SwoJUKlF4LK18ieczJiTo60f95UNwLwGlo5i2boRfSAjD8dmCm1
tLrOteyeCDb5m4P83KesvDk/AoGBAK0Kt9cUq/+pBOOcZ8uMtLtjJX0bLu+WuptL
oERDw2/h7GQQAN5IUErgDE7X1ylVytrsb719BAzM4zvXnWy6eRh4PH/SxGRBHrZQ
X+49pvZH4OtPQnlovXBCfvbdMNDxwtejUEDo8DPh53X+ZzR8z7IY9qy0r9G5tKo8
bdq1JAWJAoGAEAs3kJDX7Luxapka81xEm8NrFyjijBOYew9DUIqbgQsnj5vQ8H2v
k6jvXAMgb23vIgXuFR55fEl4O5EH7JWqMxl2xx0mQ8eQwo/G5uZiaS9ZT5xTLTJ+
hbwW5wUt+W//6qhcVtQj+0EHJfPT7VPQjzTFd0rBx0YLf0FX5SsOFyo=
-----END RSA PRIVATE KEY-----
"""

register(FamilyFactory)
register(FamilyMemberFactory)
register(BabyFactory)
register(IssuedTokenFactory)


@pytest.fixture
async def app():
    # pylint: disable=redefined-outer-name
    app = await init_app()
    exclude_tables = ["alembic_version"]

    meta = models.meta
    async with app['db'].acquire() as conn:
        for table in reversed(meta.sorted_tables):
            if table.name not in exclude_tables:
                await conn.execute(table.delete())

    yield app

    await app.shutdown()
    await app.cleanup()


@pytest.fixture
# pylint: disable=redefined-outer-name
async def cli(app, aiohttp_client):
    return await aiohttp_client(app)


@pytest.fixture
def make_headers():
    def _make_headers(uuid: UUID):
        token = jwt.encode({"user_claims": {"role": "user", "uuid": str(uuid)}},
                           key=TEST_JWT_PRIVATE_KEY,
                           algorithm="RS256")
        return {
            'content-type': 'application/json',
            'authorization': f'Bearer {token.decode("utf-8")}'
        }

    return _make_headers


@pytest.fixture
def make_tech_headers():
    def _make_tech_headers(uuid: UUID):
        token = jwt.encode({"user_claims": {"role": "tech", "uuid": str(uuid), "resources": ["family_read"]}},
                           key=TEST_JWT_PRIVATE_KEY,
                           algorithm="RS256")
        return {
            'content-type': 'application/json',
            'authorization': f'Bearer {token.decode("utf-8")}'
        }

    return _make_tech_headers


@pytest.fixture
# pylint: disable=redefined-outer-name
async def default_family_with_member(app: web.Application, family_factory, family_member_factory):
    user_uuid = str(uuid4())
    async with app['db'].acquire() as conn:
        family = family_factory.create()
        family['id'] = await family_repository.insert_family(family, conn)
        family_member = family_member_factory.create(family_id=family['id'], user_uuid=user_uuid)
        family_member['id'] = await family_member_repository.insert_family_member(family_member, conn)

    return user_uuid, family, family_member
