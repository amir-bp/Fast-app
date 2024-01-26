
from tortoise import Tortoise


async def db_conn():
    await Tortoise.init(
        db_url='postgres://amir:passcode@localhost:5432/lamp',
        modules= {'models': ['app.models']}
    )
    await Tortoise.generate_schemas()

async def db_close():
    await Tortoise.close_connections()