from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select


from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.ORMmodels import Section
from src.database import get_session
from src.database_async import get_async_session
from src.pydanticSchemas import SectionCreate, SectionOut

router = APIRouter()
# src/CRUD/sections.py

# ASYNC
@router.post("/sections/", response_model=SectionOut)
async def create_section(data: SectionCreate, session: AsyncSession = Depends(get_async_session)):
    section = Section(**data.dict())
    session.add(section)
    await session.commit()
    await session.refresh(section)
    return section

@router.get("/sections/", response_model=List[SectionOut])
async def get_all_sections(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Section))
    return result.scalars().all()

@router.get("/sections/{section_id}", response_model=SectionOut)
async def get_section(section_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Section).where(Section.id == section_id))
    section = result.scalar_one_or_none()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section

@router.put("/sections/{section_id}", response_model=SectionOut)
async def update_section(section_id: int, data: SectionCreate, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Section).where(Section.id == section_id))
    section = result.scalar_one_or_none()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(section, key, value)
    await session.commit()
    await session.refresh(section)
    return section

@router.delete("/sections/{section_id}")
async def delete_section(section_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Section).where(Section.id == section_id))
    section = result.scalar_one_or_none()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    await session.delete(section)
    await session.commit()
    return {"status": "section deleted"}


# SYNC
# @router.post("/sections/", response_model=SectionOut)
# def create_section(data: SectionCreate, session: Session = Depends(get_session)):
#     section = Section(**data.dict())
#     session.add(section)
#     session.commit()
#     session.refresh(section)
#     return section
#
# @router.get("/sections/", response_model=List[SectionOut])
# def get_all_sections(session: Session = Depends(get_session)):
#     result = session.execute(select(Section))
#     return result.scalars().all()
#
# @router.get("/sections/{section_id}", response_model=SectionOut)
# def get_section(section_id: int, session: Session = Depends(get_session)):
#     section = session.get(Section, section_id)
#     if not section:
#         raise HTTPException(status_code=404, detail="Section not found")
#     return section
#
# @router.put("/sections/{section_id}", response_model=SectionOut)
# def update_section(section_id: int, data: SectionCreate, session: Session = Depends(get_session)):
#     section = session.get(Section, section_id)
#     if not section:
#         raise HTTPException(status_code=404, detail="Section not found")
#     for key, value in data.dict(exclude_unset=True).items():
#         setattr(section, key, value)
#     session.commit()
#     session.refresh(section)
#     return section
#
# @router.delete("/sections/{section_id}")
# def delete_section(section_id: int, session: Session = Depends(get_session)):
#     section = session.get(Section, section_id)
#     if not section:
#         raise HTTPException(status_code=404, detail="Section not found")
#     session.delete(section)
#     session.commit()
#     return {"status": "section deleted"}
