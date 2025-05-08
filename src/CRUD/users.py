from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.ORMmodels import User, Base
from src.database import get_session, engine

# from src.database_async import get_async_session

router = APIRouter()
# ASYNC
# @router.post("/users/{user_id}")
# async def create_user(user_id: str, session: AsyncSession = Depends(get_async_session)):
#     result = await session.execute(select(User).where(User.id == user_id))
#     user = result.scalar_one_or_none()
#     if user:
#         return {"status": "already exists"}
#     new_user = User(id=user_id)
#     session.add(new_user)
#     await session.commit()
#     return {"status": "user created"}
#
# @router.delete("/users/{user_id}")
# async def delete_user(user_id: str, session: AsyncSession = Depends(get_async_session)):
#     result = await session.execute(select(User).where(User.id == user_id))
#     user = result.scalar_one_or_none()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     await session.delete(user)
#     await session.commit()
#     return {"status": "user deleted"}


# @router.post("/setup_database")
# def setup_database():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     return {"success": True}

# SYNC
@router.post("/users/{user_id}")
def create_user(user_id: str, session: Session = Depends(get_session)):
    user = session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user:
        return {"status": "already exists"}

    new_user = User(id=user_id)
    session.add(new_user)
    session.commit()
    return {"status": "user created"}

@router.delete("/users/{user_id}")
def delete_user(user_id: str, session: Session = Depends(get_session)):
    user = session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    return {"status": "user deleted"}
