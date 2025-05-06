from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.ORMmodels import User, Favorite, Meditation, Section
from src.database import get_session
from src.pydanticSchemas import MeditationOut, MeditationBase, MeditationCreate

router = APIRouter()

@router.post("/meditations/", response_model=MeditationOut)
def create_meditation(data: MeditationCreate, session: Session = Depends(get_session)):
    section = session.get(Section, data.section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    m = Meditation(**data.dict())
    session.add(m)
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
        section=section,
        download_url=m.download_url()
    )

@router.get("/meditations/", response_model=List[MeditationOut])
def get_all_meditations(session: Session = Depends(get_session)):
    result = session.execute(select(Meditation).join(Meditation.section))
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
def get_meditation(meditation_id: int, session: Session = Depends(get_session)):
    m = session.get(Meditation, meditation_id)
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
def update_meditation(meditation_id: int, data: MeditationBase, session: Session = Depends(get_session)):
    m = session.get(Meditation, meditation_id)
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

@router.delete("/meditations/{meditation_id}")
def delete_meditation(meditation_id: int, session: Session = Depends(get_session)):
    m = session.get(Meditation, meditation_id)
    if not m:
        raise HTTPException(status_code=404, detail="Meditation not found")
    session.delete(m)
    session.commit()
    return {"status": "meditation deleted"}
# ---------- FAVORITES ----------

@router.post("/favorites/{user_id}/{meditation_id}")
async def add_favorite(user_id: str, meditation_id: int, session: Session = Depends(get_session)):
    session.add(Favorite(user_id=user_id, meditation_id=meditation_id))
    session.commit()
    return {"status": "added to favorites"}

@router.delete("/favorites/{user_id}/{meditation_id}")
def remove_favorite(user_id: str, meditation_id: int, session: Session = Depends(get_session)):
    result = session.execute(
        select(Favorite).where(Favorite.user_id == user_id, Favorite.meditation_id == meditation_id)
    )
    fav = result.scalar_one_or_none()
    if fav:
        session.delete(fav)
        session.commit()
    return {"status": "removed"}
