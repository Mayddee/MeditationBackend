import asyncio

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy.sql.annotation import Annotated

from src.configDB import settings

router = APIRouter()

engine = create_async_engine(settings.DATABASE_URL_asyncpg, echo=False)

session_factory = async_sessionmaker(engine, class_=AsyncSession)

async def get_session() -> AsyncSession:
    async with session_factory() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass

@router.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        print(print(settings.DATABASE_URL_asyncpg)
)
    return {"success": True}