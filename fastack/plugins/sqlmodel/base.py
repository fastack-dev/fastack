from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel

from . import helpers
from .session import Session


class Model(SQLModel):
    id: Optional[int] = Field(primary_key=True, default=None)
    date_created: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow))
    date_updated: datetime = Field(sa_column=Column(DateTime, onupdate=datetime.utcnow))

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
        }

    @classmethod
    def create(cls: "Model", session: Session, **data) -> "Model":
        instance: Model = cls(**data)
        instance.save(session)
        return instance

    def save(self, session: Session, refresh: bool = True) -> "Model":
        helpers.db_add(session, self, refresh)
        return self

    def update(self, session: Session, **data) -> "Model":
        helpers.db_update(session, self, **data)
        return self

    def delete(self, session: Session) -> None:
        helpers.db_delete(session, self)
