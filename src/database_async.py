import os

from dotenv import load_dotenv
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncIterator
from src.ORMmodels import Base, User, Meditation, Section, Diary
# from src.configDB import settings

router = APIRouter()

load_dotenv()

URL_DATABASE_ASYNC = os.getenv("DATABASE_URL_ASYNC")
async_engine = create_async_engine(URL_DATABASE_ASYNC)

# async_engine = create_async_engine(settings.DATABASE_URL_asyncpg, echo=True)


session_factory = async_sessionmaker(async_engine, class_=AsyncSession)

async def get_async_session() -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session



@router.post("/setup_database")
async def setup_database():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"success": True}