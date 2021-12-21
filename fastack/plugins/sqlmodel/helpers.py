from sqlmodel import SQLModel

from .session import Session


def db_add(session: Session, instance: SQLModel, refresh: bool = True) -> SQLModel:
    atomic = session.atomic
    session.add(instance)
    if not atomic:
        session.commit()
        if refresh:
            session.refresh(instance)

    return instance


def db_update(session: Session, instance: SQLModel, **data) -> SQLModel:
    for k, v in data.items():
        setattr(instance, k, v)

    db_add(session, instance)
    return instance


def db_delete(session: Session, instance: SQLModel) -> None:
    atomic = session.atomic
    session.delete(instance)
    if not atomic:
        session.commit()
