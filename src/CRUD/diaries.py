import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from typing import List

from src.ORMmodels import User, Diary
from src.database import get_session
from src.database_async import get_async_session
from src.pydanticSchemas import DiaryOut, DiaryCreate, DiaryUpdate


# SessionDep = Depends(get_session)

router = APIRouter()
# ASYNC
@router.post("/diary/{user_id}", response_model=DiaryOut)
async def create_diary(
    user_id: str,
    data: DiaryCreate,
    session: AsyncSession = Depends(get_async_session)
):
    diary = Diary(**data.dict(), user_id=user_id)
    session.add(diary)
    await session.commit()
    await session.refresh(diary)
    return diary


@router.get("/diary/{user_id}", response_model=List[DiaryOut])
async def get_all_diaries(
    user_id: str,
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Diary).where(Diary.user_id == user_id).order_by(Diary.date.desc()))
    return result.scalars().all()


@router.get("/diary/{user_id}/{diary_id}", response_model=DiaryOut)
async def get_diary(
    user_id: str,
    diary_id: str,
    session: AsyncSession = Depends(get_async_session)
):
    diary = await session.scalar(select(Diary).where(Diary.id == diary_id))

    if not diary or diary.user_id != user_id:
        raise HTTPException(status_code=404, detail="Diary not found")
    return diary


@router.put("/diary/{user_id}/{diary_id}", response_model=DiaryOut)
async def update_diary(
    user_id: str,
    diary_id: str,
    data: DiaryUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    diary = await session.scalar(select(Diary).where(Diary.id == diary_id))

    if not diary or diary.user_id != user_id:
        raise HTTPException(status_code=404, detail="Diary not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(diary, key, value)

    await session.commit()
    await session.refresh(diary)
    return diary


@router.delete("/diary/{user_id}/{diary_id}")
async def delete_diary(
    user_id: str,
    diary_id: str,
    session: AsyncSession = Depends(get_async_session)
):
    diary = await session.scalar(select(Diary).where(Diary.id == diary_id))

    if not diary or diary.user_id != user_id:
        raise HTTPException(status_code=404, detail="Diary not found")

    await session.delete(diary)
    await session.commit()
    return {"status": "deleted"}


#SYNC

# @router.post("/diary/{user_id}", response_model=DiaryOut)
# def create_diary(user_id: str, data: DiaryCreate, session: Session = Depends(get_session)):
#     diary = Diary(**data.dict(), user_id=user_id)
#     session.add(diary)
#     session.commit()
#     session.refresh(diary)
#     return diary
#
# @router.get("/diary/{user_id}", response_model=list[DiaryOut])
# def get_all_diaries(user_id: str, session: Session = Depends(get_session)):
#     return session.query(Diary).filter(Diary.user_id == user_id).all()
#
# @router.get("/diary/{user_id}/{diary_id}", response_model=DiaryOut)
# def get_diary(user_id: str, diary_id: str, session: Session = Depends(get_session)):
#     diary = session.get(Diary, diary_id)
#     if not diary or diary.user_id != user_id:
#         raise HTTPException(status_code=404, detail="Diary not found")
#     return diary
#
# @router.put("/diary/{user_id}/{diary_id}", response_model=DiaryOut)
# def update_diary(user_id: str, diary_id: str, data: DiaryUpdate, session: Session = Depends(get_session)):
#     diary = session.get(Diary, diary_id)
#     if not diary or diary.user_id != user_id:
#         raise HTTPException(status_code=404, detail="Diary not found")
#     for key, value in data.dict(exclude_unset=True).items():
#         setattr(diary, key, value)
#     session.commit()
#     session.refresh(diary)
#     return diary
#
# @router.delete("/diary/{user_id}/{diary_id}")
# def delete_diary(user_id: str, diary_id: str, session: Session = Depends(get_session)):
#     diary = session.get(Diary, diary_id)
#     if not diary or diary.user_id != user_id:
#         raise HTTPException(status_code=404, detail="Diary not found")
#     session.delete(diary)
#     session.commit()
#     return {"status": "deleted"}
