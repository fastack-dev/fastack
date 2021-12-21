from typing import Any, Mapping, MutableMapping, Optional, Type, Union

from sqlalchemy.engine import Engine
from sqlalchemy.engine.base import Connection
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import SessionTransaction
from sqlmodel import Session as _Session


class Session(_Session):
    def __init__(
        self,
        bind: Optional[Union[Connection, Engine]] = None,
        autoflush: bool = True,
        future: bool = False,
        expire_on_commit: bool = True,
        autocommit: bool = False,
        twophase: bool = False,
        binds: Optional[Mapping[Any, Union[Connection, Engine]]] = None,
        enable_baked_queries: bool = True,
        info: Optional[MutableMapping[Any, Any]] = None,
        query_cls: Optional[Type[Query]] = None,
    ) -> None:
        super().__init__(
            bind=bind,
            autoflush=autoflush,
            future=future,
            expire_on_commit=expire_on_commit,
            autocommit=autocommit,
            twophase=twophase,
            binds=binds,
            enable_baked_queries=enable_baked_queries,
            info=info,
            query_cls=query_cls,
        )
        self.atomic: bool = False

    def begin(self, subtransactions=False, nested=False, **kwds) -> SessionTransaction:
        self.atomic = True
        return super().begin(subtransactions=subtransactions, nested=nested, **kwds)
