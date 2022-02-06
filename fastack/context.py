import typing as t
from contextvars import ContextVar, Token
from types import TracebackType

from asgi_lifespan import LifespanManager
from fastapi import Request, WebSocket

if t.TYPE_CHECKING:
    from .app import Fastack  # pragma: no cover

_app_ctx_stack: ContextVar["Fastack"] = ContextVar("_app_ctx_stack")
_request_ctx_stack: ContextVar[Request] = ContextVar("_request_ctx_stack")
_websocket_ctx_stack: ContextVar[WebSocket] = ContextVar("_websocket_ctx_stack")


class AppContext:
    def __init__(self, app: "Fastack", *, with_lifespan: bool = False) -> None:
        self.app = app
        self.with_lifespan = with_lifespan
        self._lm: t.Optional[LifespanManager] = None
        self._token: t.Optional[Token] = None

    def push(self):
        if self._token:
            return

        self._token = _app_ctx_stack.set(self.app)

    def pop(self):
        if self._token:
            _app_ctx_stack.reset(self._token)

    async def __aenter__(self):
        if self.with_lifespan:
            self._lm = LifespanManager(self.app)
            await self._lm.__aenter__()
        self.push()
        return self

    async def __aexit__(self, exc_type: type, exc_value: Exception, tb: TracebackType):
        self.pop()
        if self.with_lifespan:
            await self._lm.__aexit__(exc_type, exc_value, tb)  # type: ignore[union-attr]
