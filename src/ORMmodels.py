from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import uuid

from src.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)

    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan",
        passive_deletes=True)
    diaries = relationship("Diary", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)

    # thoughts = relationship("SharedThought", back_populates="user", cascade="all, delete-orphan",
    #     passive_deletes=True)


class Section(Base):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    duration = Column(String, nullable=True)         # e.g. "3–10 MIN"
    image_url = Column(String, nullable=True)        # Google Drive link

    meditations = relationship("Meditation", back_populates="section")


class Meditation(Base):
    __tablename__ = "meditations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    duration_sec = Column(Integer, nullable=False)
    theme = Column(String, nullable=False)
    drive_id = Column(String, nullable=False)
    image_url = Column(String, nullable=True)  # обложка проигрывателя

    section_id = Column(Integer, ForeignKey("sections.id"))
    section = relationship("Section", back_populates="meditations")

    def download_url(self):
        return f"https://drive.google.com/uc?export=download&id={self.drive_id}"



class Favorite(Base):
    __tablename__ = "favorites"
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    meditation_id = Column(Integer, ForeignKey("meditations.id"), primary_key=True)

    user = relationship("User", back_populates="favorites")
    meditation = relationship("Meditation")

class Diary(Base):
    __tablename__ = "diaries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False)
    mood = Column(Integer, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="diaries")

# class SharedThought(Base):
#     __tablename__ = "shared_thoughts"
#     id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
#     user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"))
#     content = Column(Text, nullable=False)
#     image_url = Column(String, nullable=True)
#     meditation_id = Column(Integer, ForeignKey("meditations.id"), nullable=True)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(hours=24))
#
#     user = relationship("User", back_populates="thoughts")
#     meditation = relationship("Meditation")