from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


class Model(SQLModel):
    date_created: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow))
    date_updated: datetime = Field(sa_column=Column(DateTime, onupdate=datetime.utcnow))

    def serialize(self) -> dict:
        return {
            "date_created": self.date_created,
            "date_updated": self.date_updated,
        }
