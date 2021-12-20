from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime
from sqlalchemy.orm.session import SessionTransaction
from sqlmodel import Field, Session, SQLModel


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
    def create(cls, session: Session, **data) -> "Model":
        instance = cls(**data)
        instance.save(session)
        return instance

    def save(self, session: Session, refresh: bool = True) -> "Model":
        session.add(self)
        self._do_commit(session)
        if refresh and not self._is_atomic_transaction(session):
            session.refresh(self)

        return self

    def update(self, session: Session, **data) -> "Model":
        for k, v in data.items():
            setattr(self, k, v)

        self.save(session)
        return self

    def delete(self, session: Session) -> None:
        session.delete(self)
        self._do_commit(session)

    def _is_atomic_transaction(self, session: Session) -> bool:
        return session._transaction is not None and isinstance(
            session._transaction, SessionTransaction
        )

    def _do_commit(self, session: Session):
        if self._is_atomic_transaction(session):
            return

        session.commit()
