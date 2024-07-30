from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config import DB_USER, DB_PASS, DB_HOST, DB_NAME

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"


engine = create_async_engine(DATABASE_URL)

new_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

# Асинхронная функция для получения сессии
async def get_session():
    async with new_session() as session:
        yield session