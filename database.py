from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from typing import AsyncGenerator
from config import PORT, USER_NAME, DB_NAME, HOST, PASSWORD
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
print(SQLALCHEMY_DATABASE_URL)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base(metadata=MetaData())


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
