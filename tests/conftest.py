# import pytest
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# from async_session import Base, get_session
# from config import DB_USER, DB_PASS, DB_HOST, DB_NAME
# import asyncio
#
# # Настройка тестовой базы данных
# TEST_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/test_{DB_NAME}"
#
# @pytest.fixture(scope="session")
# async def test_engine():
#     engine = create_async_engine(TEST_DATABASE_URL, echo=True)
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield engine
#     await engine.dispose()
#
# @pytest.fixture(scope="function")
# async def test_session(test_engine):
#     session = sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)()
#     yield session
#     await session.close()
#
# @pytest.fixture(scope="function")
# async def client(test_session):
#     from fastapi.testclient import TestClient
#     from main import app
#
#     app.dependency_overrides[get_session] = lambda: test_session
#     with TestClient(app) as client:
#         yield client
