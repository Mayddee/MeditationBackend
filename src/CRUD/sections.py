from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select


from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.ORMmodels import Section
from src.database import get_session
from src.pydanticSchemas import SectionCreate, SectionOut

router = APIRouter()
# src/CRUD/sections.py

@router.post("/sections/", response_model=SectionOut)
def create_section(data: SectionCreate, session: Session = Depends(get_session)):
    section = Section(**data.dict())
    session.add(section)
    session.commit()
    session.refresh(section)
    return section

@router.get("/sections/", response_model=List[SectionOut])
def get_all_sections(session: Session = Depends(get_session)):
    result = session.execute(select(Section))
    return result.scalars().all()

@router.get("/sections/{section_id}", response_model=SectionOut)
def get_section(section_id: int, session: Session = Depends(get_session)):
    section = session.get(Section, section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section

@router.put("/sections/{section_id}", response_model=SectionOut)
def update_section(section_id: int, data: SectionCreate, session: Session = Depends(get_session)):
    section = session.get(Section, section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(section, key, value)
    session.commit()
    session.refresh(section)
    return section

@router.delete("/sections/{section_id}")
def delete_section(section_id: int, session: Session = Depends(get_session)):
    section = session.get(Section, section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    session.delete(section)
    session.commit()
    return {"status": "section deleted"}
