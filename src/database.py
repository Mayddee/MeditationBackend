# import asyncio
# import os
#
# from fastapi import Depends, APIRouter
# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase, declarative_base
# from sqlalchemy.sql.annotation import Annotated
# from dotenv import load_dotenv
#
# # from src.configDB import settings
#
# router = APIRouter()
#
# load_dotenv()
#
# URL_DATABASE = os.getenv("DATABASE_URL")
#
#
# engine = create_engine(URL_DATABASE)
#
#
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()
#
# def get_session():
#     session = SessionLocal()
#     try:
#         yield session
#     finally:
#         session.close()
#
# @router.post("/setup_database")
# def setup_database():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     return {"success": True}
