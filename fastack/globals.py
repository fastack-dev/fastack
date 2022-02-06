from contextvars import ContextVar
from typing import TYPE_CHECKING

from fastapi import Request, WebSocket
from starlette.datastructures import State

from .context import _app_ctx_stack, _request_ctx_stack, _websocket_ctx_stack
from .local import LocalProxy

if TYPE_CHECKING:
    from .app import Fastack  # pragma: no cover


def _find_object(ctx: ContextVar, err: str):
    try:
        obj = ctx.get()
        if not obj:  # pragma: no cover
            raise LookupError
    except LookupError:
        raise RuntimeError(err)

    return obj


def _get_app() -> "Fastack":
    return _find_object(_app_ctx_stack, "Working outside of application context.")


def _get_request() -> "Fastack":
    return _find_object(_request_ctx_stack, "Working outside of request context.")


def _get_websocket() -> "Fastack":
    return _find_object(_websocket_ctx_stack, "Working outside of websocket context.")


current_app: "Fastack" = LocalProxy(_get_app)
request: Request = LocalProxy(_get_request)
websocket: WebSocket = LocalProxy(_get_websocket)
state: State = LocalProxy(lambda: current_app.state)


def has_app_context():
    """
    Check if application context is active.
    """

    return bool(current_app)


def has_request_context():
    """
    Check if request context is active.
    """

    return bool(request)


def has_websocket_context():
    """
    Check if websocket context is active.
    """

    return bool(websocket)
