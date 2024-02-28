import asyncio
from sqlalchemy.ext import asyncio as async_alchemy
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import text

# With asynchronous code it's a little bit different --> you need to create an engine and then dispose of it
# in a coroutine




async def create_commit_as_go(engine: AsyncEngine):
    """ 'Commit as you go'-style: uses Engine.commit(), so we need to write conn.commit() ourselves"""
    async with engine.connect() as conn:
        """ 'Commit as you go' --> thorugh """
        await conn.execute(text("""CREATE TABLE IF NOT EXISTS test_table (x int, y int)"""))
        await conn.execute(text("""INSERT INTO test_table (x, y) VALUES (:x, :y)"""),
                           [{'x': 1, 'y': 1}, {'x': 2, 'y': 4}])
        await conn.commit()


async def begin_once(engine: AsyncEngine):
    """ 'Begin once'-style  -> automatically commits or rollbacks"""

    async with engine.begin() as conn:
        await conn.execute(text("""INSERT INTO test_table (x, y) VALUES (:x, :y)"""),
                           [{'x': 0, 'y': 1}]
                           )


async def print_table_all(engine: AsyncEngine):
    async with engine.connect() as conn:
        result = await conn.execute(text("""SELECT * FROM test_table"""))
        for i_row in result:
            print(i_row)


async def print_table_x_y(engine: AsyncEngine):
    async with engine.connect() as conn:
        result = await conn.execute(text("""SELECT x, y FROM test_table WHERE y > :y"""), [{'y': 2}])
        for i_row in result:
            print(i_row.x, i_row.y)

        await engine.dispose()


# async def print_table_orm():
#     async with Session(engine) as session:


async def main_db_core():
    """Main function to operate SQL in"""

    test_url = "postgresql+asyncpg://unstoppable:BubbaMngloa#843@/magic_test"
    engine = async_alchemy.create_async_engine(
        url=test_url,
        echo=True,
    )

    # await create_commit_as_go(engine)
    # await begin_once(engine)
    # await print_table_all(engine)
    await print_table_x_y(engine)

    await engine.dispose()  # have to dispose of an async engine

############################################################################################################


async def insert_values_and_print(async_session: async_sessionmaker[AsyncSession]) -> None:
    async with async_session.begin() as session:
        await session.execute(text("""INSERT INTO test_table (x, y) VALUES (:x, :y)"""),
                              [{'x': 21, 'y': 28}, {'x': 32, 'y': 44}]
                              )

        result = await session.execute(text("""SELECT * FROM test_table WHERE x > :x"""), [{'x': 20}])
        for row in result:
            print(row.x, row.y)


async def main_db_orm():
    """Main function to operate SQL in ORM-paradigm"""

    test_url = "postgresql+asyncpg://unstoppable:BubbaMngloa#843@/magic_test"
    engine = async_alchemy.create_async_engine(
        url=test_url,
        echo=True,
    )

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    await insert_values_and_print(async_session)
    await engine.dispose()

if __name__ == '__main__':
    # asyncio.run(main_db_core())
    asyncio.run(main_db_orm())
