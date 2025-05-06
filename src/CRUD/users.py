from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.ORMmodels import User
from src.database import SessionDep, get_session

router = APIRouter()



@router.post("/users/{user_id}")
async def create_user(user_id: str, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if user:
        return {"status": "already exists"}
    session.add(User(id=user_id))
    await session.commit()
    return {"status": "user created"}

@router.delete("/users/{user_id}")
async def delete_user(user_id: str, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)
    await session.commit()
    return {"status": "user deleted"}