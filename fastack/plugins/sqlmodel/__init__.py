from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import SessionTransaction
from sqlmodel import Session, SQLModel, create_engine

from fastack import Fastack


class DatabaseState:
    def __init__(self, engine: Engine):
        self.engine = engine

    def open(self, engine: Engine = None, **kwds) -> Session:
        engine = engine or self.engine
        return Session(self.engine, **kwds)

    def atomic(self, engine: Engine = None, **kwds) -> SessionTransaction:
        engine = engine or self.engine
        return self.open(engine, **kwds).begin()


def setup(app: Fastack):
    @app.on_event("startup")
    def on_startup():
        uri = app.state.settings.SQLALCHEMY_DATABASE_URI
        connect_args = app.state.settings.SQLALCHEMY_CONNECT_ARGS
        options = app.state.settings.SQLALCHEMY_OPTIONS
        engine = create_engine(uri, connect_args=connect_args, **options)
        app.state.db = DatabaseState(engine)
        SQLModel.metadata.create_all(engine)
