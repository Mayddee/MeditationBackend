from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import select, or_
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload

from src.ORMmodels import User, Favorite, Meditation, Section
from src.database import get_session
# from src.database_async import get_async_session
from src.pydanticSchemas import MeditationOut, MeditationBase, MeditationCreate

router = APIRouter()


# ASYNC

# @router.get("/meditations/search", response_model=List[MeditationOut])
# async def search_meditations(
#     query: str = Query(..., min_length=1),
#     session: AsyncSession = Depends(get_async_session)
# ):
#     result = await session.execute(
#         select(Meditation)
#         .options(joinedload(Meditation.section))
#         .where(
#             or_(
#                 Meditation.title.ilike(f"%{query}%"),
#                 Meditation.theme.ilike(f"%{query}%")
#             )
#         )
#     )
#     meditations = result.scalars().all()
#
#     return [
#         MeditationOut(
#             id=m.id,
#             title=m.title,
#             duration_sec=m.duration_sec,
#             theme=m.theme,
#             drive_id=m.drive_id,
#             image_url=m.image_url,
#             section_id=m.section_id,
#             section=m.section,
#             download_url=m.download_url()
#         )
#         for m in meditations
#     ]
#
# @router.post("/meditations/", response_model=MeditationOut)
# async def create_meditation(data: MeditationCreate, session: AsyncSession = Depends(get_async_session)):
#     meditation = Meditation(**data.dict())
#     session.add(meditation)
#     await session.flush()
#     await session.refresh(meditation)
#
#     return MeditationOut(
#         id=meditation.id,
#         title=meditation.title,
#         duration_sec=meditation.duration_sec,
#         theme=meditation.theme,
#         drive_id=meditation.drive_id,
#         image_url=meditation.image_url,
#         section_id=meditation.section_id,
#         section=None,  # 👈 либо None, либо загрузи отдельно через select(...) с joinedload
#         download_url=meditation.download_url()
#     )
#
# @router.get("/meditations/", response_model=List[MeditationOut])
# async def get_all_meditations(session: AsyncSession = Depends(get_async_session)):
#     result = await session.execute(
#         select(Meditation).options(joinedload(Meditation.section))
#     )
#     meditations = result.scalars().all()
#     return [
#         MeditationOut(
#             id=m.id,
#             title=m.title,
#             duration_sec=m.duration_sec,
#             theme=m.theme,
#             drive_id=m.drive_id,
#             image_url=m.image_url,
#             section_id=m.section_id,
#             section=m.section,
#             download_url=m.download_url()
#         )
#         for m in meditations
#     ]
#
# @router.get("/meditations/{meditation_id}", response_model=MeditationOut)
# async def get_meditation(meditation_id: int, session: AsyncSession = Depends(get_async_session)):
#     result = await session.execute(
#         select(Meditation).options(joinedload(Meditation.section)).where(Meditation.id == meditation_id)
#     )
#     m = result.scalar_one_or_none()
#     if not m:
#         raise HTTPException(status_code=404, detail="Meditation not found")
#     return MeditationOut(
#         id=m.id,
#         title=m.title,
#         duration_sec=m.duration_sec,
#         theme=m.theme,
#         drive_id=m.drive_id,
#         image_url=m.image_url,
#         section_id=m.section_id,
#         section=m.section,
#         download_url=m.download_url()
#     )
#
# @router.put("/meditations/{meditation_id}", response_model=MeditationOut)
# async def update_meditation(meditation_id: int, data: MeditationBase, session: AsyncSession = Depends(get_async_session)):
#     result = await session.execute(select(Meditation).where(Meditation.id == meditation_id))
#     m = result.scalar_one_or_none()
#     if not m:
#         raise HTTPException(status_code=404, detail="Meditation not found")
#     for key, value in data.dict().items():
#         setattr(m, key, value)
#     await session.commit()
#     await session.refresh(m)
#     return MeditationOut(
#         id=m.id,
#         title=m.title,
#         duration_sec=m.duration_sec,
#         theme=m.theme,
#         drive_id=m.drive_id,
#         image_url=m.image_url,
#         section_id=m.section_id,
#         section=m.section,
#         download_url=m.download_url()
#     )
#
# @router.delete("/meditations/{meditation_id}")
# async def delete_meditation(meditation_id: int, session: AsyncSession = Depends(get_async_session)):
#     result = await session.execute(select(Meditation).where(Meditation.id == meditation_id))
#     m = result.scalar_one_or_none()
#     if not m:
#         raise HTTPException(status_code=404, detail="Meditation not found")
#     await session.delete(m)
#     await session.commit()
#     return {"status": "meditation deleted"}
#
# # ---------- FAVORITES ----------
#
# @router.post("/favorites/{user_id}/{meditation_id}")
# async def add_favorite(user_id: str, meditation_id: int, session: AsyncSession = Depends(get_async_session)):
#     session.add(Favorite(user_id=user_id, meditation_id=meditation_id))
#     await session.commit()
#     return {"status": "added to favorites"}
#
# @router.delete("/favorites/{user_id}/{meditation_id}")
# async def remove_favorite(user_id: str, meditation_id: int, session: AsyncSession = Depends(get_async_session)):
#     result = await session.execute(
#         select(Favorite).where(Favorite.user_id == user_id, Favorite.meditation_id == meditation_id)
#     )
#     fav = result.scalar_one_or_none()
#     if fav:
#         await session.delete(fav)
#         await session.commit()
#     return {"status": "removed"}



# SYNC
@router.get("/meditations/search", response_model=list[MeditationOut], tags=["Meditations"])
def search_meditations(query: str = Query(..., min_length=1), session: Session = Depends(get_session)):
    result = session.execute(
        select(Meditation).options(joinedload(Meditation.section)).where(
            or_(Meditation.title.ilike(f"%{query}%"), Meditation.theme.ilike(f"%{query}%"))
        )
    )
    return [
        MeditationOut(
            id=m.id,
            title=m.title,
            duration_sec=m.duration_sec,
            theme=m.theme,
            drive_id=m.drive_id,
            image_url=m.image_url,
            section_id=m.section_id,
            section=m.section,
            download_url=m.download_url()
        ) for m in result.scalars()
    ]

@router.post("/meditations/", response_model=MeditationOut, tags=["Meditations"])
def create_meditation(data: MeditationCreate, session: Session = Depends(get_session)):
    meditation = Meditation(**data.dict())
    session.add(meditation)
    session.commit()
    session.refresh(meditation)
    return MeditationOut(
        id=meditation.id,
        title=meditation.title,
        duration_sec=meditation.duration_sec,
        theme=meditation.theme,
        drive_id=meditation.drive_id,
        image_url=meditation.image_url,
        section_id=meditation.section_id,
        section=None,
        download_url=meditation.download_url()
    )

@router.get("/meditations/", response_model=list[MeditationOut], tags=["Meditations"])
def get_all_meditations(session: Session = Depends(get_session)):
    result = session.execute(select(Meditation).options(joinedload(Meditation.section)))
    return [
        MeditationOut(
            id=m.id,
            title=m.title,
            duration_sec=m.duration_sec,
            theme=m.theme,
            drive_id=m.drive_id,
            image_url=m.image_url,
            section_id=m.section_id,
            section=m.section,
            download_url=m.download_url()
        ) for m in result.scalars()
    ]

@router.get("/meditations/{meditation_id}", response_model=MeditationOut, tags=["Meditations"])
def get_meditation(meditation_id: int, session: Session = Depends(get_session)):
    result = session.execute(select(Meditation).options(joinedload(Meditation.section)).where(Meditation.id == meditation_id))
    m = result.scalar_one_or_none()
    if not m:
        raise HTTPException(status_code=404, detail="Meditation not found")
    return MeditationOut(
        id=m.id,
        title=m.title,
        duration_sec=m.duration_sec,
        theme=m.theme,
        drive_id=m.drive_id,
        image_url=m.image_url,
        section_id=m.section_id,
        section=m.section,
        download_url=m.download_url()
    )

@router.put("/meditations/{meditation_id}", response_model=MeditationOut, tags=["Meditations"])
def update_meditation(meditation_id: int, data: MeditationBase, session: Session = Depends(get_session)):
    result = session.execute(select(Meditation).where(Meditation.id == meditation_id))
    m = result.scalar_one_or_none()
    if not m:
        raise HTTPException(status_code=404, detail="Meditation not found")
    for key, value in data.dict().items():
        setattr(m, key, value)
    session.commit()
    session.refresh(m)
    return MeditationOut(
        id=m.id,
        title=m.title,
        duration_sec=m.duration_sec,
        theme=m.theme,
        drive_id=m.drive_id,
        image_url=m.image_url,
        section_id=m.section_id,
        section=m.section,
        download_url=m.download_url()
    )

@router.delete("/meditations/{meditation_id}", tags=["Meditations"])
def delete_meditation(meditation_id: int, session: Session = Depends(get_session)):
    result = session.execute(select(Meditation).where(Meditation.id == meditation_id))
    m = result.scalar_one_or_none()
    if not m:
        raise HTTPException(status_code=404, detail="Meditation not found")
    session.delete(m)
    session.commit()
    return {"status": "meditation deleted"}

@router.post("/favorites/{user_id}/{meditation_id}", tags=["Favourites"])
def add_favorite(user_id: str, meditation_id: int, session: Session = Depends(get_session)):
    session.add(Favorite(user_id=user_id, meditation_id=meditation_id))
    session.commit()
    return {"status": "added to favorites"}

@router.delete("/favorites/{user_id}/{meditation_id}", tags=["Favourites"])
def remove_favorite(user_id: str, meditation_id: int, session: Session = Depends(get_session)):
    result = session.execute(
        select(Favorite).where(Favorite.user_id == user_id, Favorite.meditation_id == meditation_id)
    )
    fav = result.scalar_one_or_none()
    if fav:
        session.delete(fav)
        session.commit()
    return {"status": "removed"}