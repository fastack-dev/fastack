import typing as t
from contextvars import ContextVar

from fastapi import Request, WebSocket

if t.TYPE_CHECKING:
    from .app import Fastack  # pragma: no cover

_app_ctx_stack: ContextVar["Fastack"] = ContextVar("_app_ctx_stack")
_request_ctx_stack: ContextVar[Request] = ContextVar("_request_ctx_stack")
_websocket_ctx_stack: ContextVar[WebSocket] = ContextVar("_websocket_ctx_stack")
