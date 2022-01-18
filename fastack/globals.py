from typing import TYPE_CHECKING

from fastapi import Request, WebSocket
from starlette.datastructures import State
from werkzeug.local import LocalProxy

from .context import _app_ctx_stack, _request_ctx_stack, _websocket_ctx_stack

if TYPE_CHECKING:
    from .app import Fastack  # pragma: no cover


def _get_app() -> "Fastack":
    app = _app_ctx_stack.get()
    if not app:
        raise RuntimeError("Working outside of application context.")
    return app


current_app: "Fastack" = LocalProxy(_get_app)
request: Request = LocalProxy(lambda: _request_ctx_stack.get())
websocket: WebSocket = LocalProxy(lambda: _websocket_ctx_stack.get())
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
