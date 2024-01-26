from tortoise import Tortoise, run_async
from database.connection import db_conn


async def main():
    await db_conn()
    await Tortoise.generate_schemas()


if __name__ == '__main__':
    run_async(main())


