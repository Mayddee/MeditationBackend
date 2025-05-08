
from pydantic import BaseModel
from datetime import datetime
import uvicorn


class UserOut(BaseModel):
    id: str

    class Config:
        from_attributes = True

class SectionCreate(BaseModel):
    title: str
    subtitle: str | None = None
    duration: str | None = None
    image_url: str | None = None

class SectionOut(SectionCreate):
    id: int  # только на выходе

    class Config:
        from_attributes = True
# --- Meditation ---
class MeditationBase(BaseModel):
    title: str | None = None
    duration_sec: int
    theme: str | None = None
    drive_id: str | None = None
    image_url: str | None = None
    section_id: int | None = None

class MeditationCreate(MeditationBase):
    pass

class MeditationOut(MeditationBase):
    id: int
    download_url: str
    section: SectionOut | None = None

    class Config:
        from_attributes = True
# --- Diary ---
class DiaryCreate(BaseModel):
    title: str
    content: str
    date: datetime
    mood: int

class DiaryUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    mood: int | None = None

class DiaryOut(BaseModel):
    id: str
    user_id: str
    title: str
    content: str
    date: datetime
    mood: int
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Thought ---
class ThoughtCreate(BaseModel):
    content: str
    meditation_id: str | None = None
    image_url:str | None = None

class ThoughtOut(BaseModel):
    id: str
    user_id: str
    content: str
    image_url: str | None
    meditation_id: str | None
    created_at: datetime

    class Config:
        from_attributes = True