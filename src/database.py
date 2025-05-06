import asyncio
import os

from fastapi import Depends, APIRouter
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase, declarative_base
from sqlalchemy.sql.annotation import Annotated
from dotenv import load_dotenv

# from src.configDB import settings

router = APIRouter()

load_dotenv()

URL_DATABASE = os.getenv("DATABASE_URL")


engine = create_engine(URL_DATABASE)

# engine = create_async_engine(settings.DATABASE_URL, echo=True)

# session_factory = sessionmaker(engine, class_=Session)
# session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
# def get_session() -> Session:
#     with session_factory() as session:
#         yield session
#
# SessionDep = Annotated[Session, Depends(get_session)]
#
# class Base(DeclarativeBase):
#     pass

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@router.post("/setup_database")
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {"success": True}
# def setup_database():
#     with engine.begin() as conn:
#         conn.run_sync(Base.metadata.drop_all)
#         conn.run_sync(Base.metadata.create_all)
#         # print(print(settings.DATABASE_URL_asyncpg)
#         #
#         return {"success": True}