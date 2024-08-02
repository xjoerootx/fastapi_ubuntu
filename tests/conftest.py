import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app

DATABASE_URL = "postgresql+asyncpg://joeroot:586653182@localhost/test1_db"
engine = create_async_engine(DATABASE_URL, echo=True)
try:
    from main import app
except (NameError, ImportError):
    raise AssertionError('НЕ НАЙДЕНО ПРИЛОЖЕНИЕ')
@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
@pytest.fixture(scope="session", autouse=True)
async def test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def session():
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


# import pytest
# from httpx import AsyncClient, ASGITransport
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# from sqlalchemy.orm import sessionmaker
# from database import Base
# from main import app
#
# DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/test1_db"
# engine = create_async_engine(DATABASE_URL, echo=True)
#
# @pytest.fixture(scope="session")
# async def async_client():
#     async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
#         yield client
#
# @pytest.fixture(scope="function", autouse=True)
# async def setup_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#
# @pytest.fixture(scope="function")
# async def session():
#     async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
#     async with async_session() as session:
#         yield session