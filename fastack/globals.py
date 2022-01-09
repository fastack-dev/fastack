from typing import TYPE_CHECKING

from fastapi import Request, WebSocket
from starlette.datastructures import State
from werkzeug.local import LocalProxy

from .context import _app_ctx_stack, _request_ctx_stack, _websocket_ctx_stack

if TYPE_CHECKING:
    from .app import Fastack


def _get_state() -> State:
    """
    Get state from application or request.
    """

    state = None
    if current_app and not request:
        state = current_app.state
    elif request:
        state = request.state
    return state


current_app: "Fastack" = LocalProxy(lambda: _app_ctx_stack.top)
request: Request = LocalProxy(lambda: _request_ctx_stack.top)
websocket: WebSocket = LocalProxy(lambda: _websocket_ctx_stack.top)
state: State = LocalProxy(lambda: _get_state())


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
