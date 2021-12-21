from sqlalchemy.engine import Engine
from sqlmodel import SQLModel, create_engine

from fastack import Fastack

from .session import Session


class DatabaseState:
    def __init__(self, engine: Engine):
        self.engine = engine

    def open(self, engine: Engine = None, **kwds) -> Session:
        engine = engine or self.engine
        return Session(self.engine, **kwds)


def setup(app: Fastack):
    @app.on_event("startup")
    def on_startup():
        uri = app.state.settings.SQLALCHEMY_DATABASE_URI
        connect_args = app.state.settings.SQLALCHEMY_CONNECT_ARGS
        options = app.state.settings.SQLALCHEMY_OPTIONS
        engine = create_engine(uri, connect_args=connect_args, **options)
        app.state.db = DatabaseState(engine)
        SQLModel.metadata.create_all(engine)
