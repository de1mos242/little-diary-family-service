from aiohttp import web
from aiohttp_apispec import docs

from family_api.models import families_table


class HealthView(web.View):

    @docs(summary="Health check endpoint",
          responses={200: "Service is health",
                     500: "Service has problems"})
    async def get(self):
        async with self.request.app['db'].acquire() as conn:
            await (await conn.execute(families_table.select())).first()
        return web.Response(status=200)
