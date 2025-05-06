from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.ORMmodels import User, Favorite, Meditation, Section
from src.database import SessionDep, get_session
from src.pydanticSchemas import MeditationOut, MeditationBase, MeditationCreate

router = APIRouter()

@router.post("/meditations/", response_model=MeditationOut)
async def create_meditation(data: MeditationCreate, session: AsyncSession = Depends(get_session)):
    section = await session.get(Section, data.section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    m = Meditation(**data.dict())
    session.add(m)
    await session.commit()
    await session.refresh(m)

    return MeditationOut(
        id=m.id,
        title=m.title,
        duration_sec=m.duration_sec,
        theme=m.theme,
        drive_id=m.drive_id,
        image_url=m.image_url,
        section_id=m.section_id,
        section=section,
        download_url=m.download_url()
    )

@router.get("/meditations/", response_model=List[MeditationOut])
async def get_all_meditations(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Meditation).join(Meditation.section))
    meditations = result.scalars().all()
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
        )
        for m in meditations
    ]

@router.get("/meditations/{meditation_id}", response_model=MeditationOut)
async def get_meditation(meditation_id: int, session: AsyncSession = Depends(get_session)):
    m = await session.get(Meditation, meditation_id)
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

@router.put("/meditations/{meditation_id}", response_model=MeditationOut)
async def update_meditation(meditation_id: int, data: MeditationBase, session: AsyncSession = Depends(get_session)):
    m = await session.get(Meditation, meditation_id)
    if not m:
        raise HTTPException(status_code=404, detail="Meditation not found")
    for key, value in data.dict().items():
        setattr(m, key, value)
    await session.commit()
    await session.refresh(m)
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

@router.delete("/meditations/{meditation_id}")
async def delete_meditation(meditation_id: int, session: AsyncSession = Depends(get_session)):
    m = await session.get(Meditation, meditation_id)
    if not m:
        raise HTTPException(status_code=404, detail="Meditation not found")
    await session.delete(m)
    await session.commit()
    return {"status": "meditation deleted"}
# ---------- FAVORITES ----------

@router.post("/favorites/{user_id}/{meditation_id}")
async def add_favorite(user_id: str, meditation_id: int, session: AsyncSession = Depends(get_session)):
    session.add(Favorite(user_id=user_id, meditation_id=meditation_id))
    await session.commit()
    return {"status": "added to favorites"}

@router.delete("/favorites/{user_id}/{meditation_id}")
async def remove_favorite(user_id: str, meditation_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Favorite).where(Favorite.user_id == user_id, Favorite.meditation_id == meditation_id)
    )
    fav = result.scalar_one_or_none()
    if fav:
        await session.delete(fav)
        await session.commit()
    return {"status": "removed"}
