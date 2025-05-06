from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.ORMmodels import User
from src.database import get_session

router = APIRouter()



@router.post("/users/{user_id}")
def create_user(user_id: str, session: Session = Depends(get_session)):
    user =  session.get(User, user_id)
    if user:
        return {"status": "already exists"}
    session.add(User(id=user_id))
    session.commit()
    return {"status": "user created"}

@router.delete("/users/{user_id}")
def delete_user(user_id: str, session: Session = Depends(get_session)):
    user =  session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"status": "user deleted"}