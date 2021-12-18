from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import SessionTransaction
from sqlmodel import Session, SQLModel, create_engine

from fastack import Fastack


class DatabaseConnection:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.session: Session = Session(self.engine)
        self.transaction: SessionTransaction = None

    def __enter__(self):
        self.transaction = self.session.begin()
        return self.transaction

    def __exit__(self, type, value, traceback):
        self.transaction.close()


def setup(app: Fastack):
    @app.on_event("startup")
    def on_startup():
        uri = app.state.settings.SQLALCHEMY_DATABASE_URI
        connect_args = app.state.settings.SQLALCHEMY_CONNECT_ARGS
        options = app.state.settings.SQLALCHEMY_OPTIONS
        engine = create_engine(uri, connect_args=connect_args, **options)
        app.state.open_db = DatabaseConnection(engine)
        SQLModel.metadata.create_all(engine)
