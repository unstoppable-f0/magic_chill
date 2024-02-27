import asyncio
from sqlalchemy.ext import asyncio as async_alchemy
from sqlalchemy import text


test_url = "postgresql+asyncpg://unstoppable:BubbaMngloa#843@/magic_test"
engine = async_alchemy.create_async_engine(
    url=test_url,
    echo=True,
    )


async def commit_as_go():
    """ 'Commit as you go'-style: uses Engine.commit(), so we need to write conn.commit() ourselves"""
    async with engine.connect() as conn:
        """ 'Commit as you go' --> thorugh """
        await conn.execute(text("""CREATE TABLE IF NOT EXISTS test_table (x int, y int)"""))
        await conn.execute(text("""INSERT INTO test_table (x, y) VALUES (:x, :y)"""),
                           [{'x': 1, 'y': 1}, {'x': 2, 'y': 4}])
        await conn.commit()


async def begin_once():
    """ 'Begin once'-style  -> automatically commits or rollbacks"""

    async with engine.begin() as conn:
        await conn.execute(text("""INSERT INTO test_table (x, y) VALUES (:x, :y)"""),
                           [{'x': 0, 'y': 1}]
                           )


async def print_table():
    async with engine.connect() as conn:
        result = await conn.execute(text("""SELECT * FROM test_table"""))
        for i_row in result:
            print(i_row)


async def main_db():
    # await commit_as_go()
    await begin_once()
    await print_table()


if __name__ == '__main__':
    asyncio.run(main_db())
