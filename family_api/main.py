import asyncio

from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_jwt import JWTMiddleware
from aiopg.sa import create_engine

from family_api.config import Config
from family_api.middlewares import get_current_user_middleware
from family_api.routes import setup_routes

SECURITY_WHITELIST = ['/swagger-ui', '/static*', '/api/docs*']


async def create_db_connection():
    return await create_engine(Config.DATABASE_URI, echo=True)


def create_jwt_middleware():
    return JWTMiddleware(secret_or_pub_key=Config.JWT_PUBLIC_KEY,
                         request_property='token_data',
                         credentials_required=True,
                         whitelist=SECURITY_WHITELIST)


def create_current_user_middleware():
    return get_current_user_middleware(SECURITY_WHITELIST)


async def init_app():
    jwt_middleware = create_jwt_middleware()
    current_user_middleware = create_current_user_middleware()
    app = web.Application(middlewares=[jwt_middleware, current_user_middleware])
    setup_routes(app)
    setup_aiohttp_apispec(app=app, title="Family service", version="v1", swagger_path='/swagger-ui',
                          securityDefinitions={"jwt": {"type": "apiKey",
                                                       "schema": "bearer",
                                                       "bearerFormat": "JWT",
                                                       "name": "Authorization",
                                                       "in": "header"}},
                          security=[{"jwt": []}])
    app['db'] = await create_db_connection()
    app.on_cleanup.append(close_pg)
    return app


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


def main():
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app)


if __name__ == '__main__':
    main()
