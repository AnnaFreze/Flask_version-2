import datetime
import os
from atexit import register
from typing import List, Optional
from sqlalchemy import DateTime, Integer, String, create_engine, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "psgegel")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "advs")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")


engine = create_engine(
    f"postgresql://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    # password: Mapped[str] = mapped_column(String(72), nullable=False)

    advs: Mapped[list["Adv"]] = relationship(back_populates="user",)

    @property
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "advs": [adv.json for adv in self.advs]
          }


class Adv(Base):
    __tablename__ = "advs"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=False)
    content: Mapped[Optional[str]] = mapped_column(String)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="advs", )

    @property
    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id
          }

Base.metadata.create_all(bind=engine)
register(engine.dispose)