from datetime import datetime
from enum import Enum
from typing import Optional, List

from sqlalchemy import String, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        columns = self.__table__.columns.keys()
        values = ", ".join(f"{col}={getattr(self, col)!r}" for col in columns)
        return f"{self.__class__.__name__}({values})"


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(50))
    phone_number: Mapped[Optional[str]] = mapped_column(String(20))

    applications: Mapped[List["Application"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Event(Base):
    __tablename__ = "events"

    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]]
    event_time: Mapped[datetime] = mapped_column(DateTime)
    registration_due: Mapped[datetime] = mapped_column(DateTime)
    location: Mapped[str] = mapped_column(String(100))
    image_url: Mapped[Optional[str]] = mapped_column()

    applications: Mapped[List["Application"]] = relationship(
        back_populates="event",
        cascade="all, delete-orphan"
    )


class Status(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"


class Application(Base):
    __tablename__ = "applications"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))
    team_name: Mapped[str]
    team_size: Mapped[int]
    status: Mapped[Status] = mapped_column(default=Status.PENDING)

    user = relationship(
        "User",
        back_populates="applications",
    )
    event = relationship(
        "Event",
        back_populates="applications",
    )


class Admin(Base):
    __tablename__ = "admins"

    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
