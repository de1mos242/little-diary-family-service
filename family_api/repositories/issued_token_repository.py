from family_api.models import issued_tokens_table


async def insert_token(issued_token, conn):
    return await conn.scalar(issued_tokens_table.insert().values(issued_token))


async def get_token(token, conn):
    return await(await conn.execute(issued_tokens_table.select().where(issued_tokens_table.c.token == token))).first()


async def delete_issued_token(token_id, conn):
    await conn.execute(issued_tokens_table.delete().where(issued_tokens_table.c.id == token_id))
