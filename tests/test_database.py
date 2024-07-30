import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from database import Base

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/test1_db"

@pytest.fixture(scope="module")
async def test_db():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def session(test_db):
    async_session = sessionmaker(test_db, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session