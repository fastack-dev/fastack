from typing import TYPE_CHECKING

from .base import (
    BaseMiddleware,
    ProcessRequestFunc,
    ProcessResponseFunc,
    ProcessWebSocketFunc,
)

if TYPE_CHECKING:
    from ..app import Fastack


class MiddlewareManager:
    """
    Middleware Manager which allows you to create middleware with functions.
    """

    def __init__(self, app: "Fastack"):
        self.app = app

    def process_request(self, func: ProcessRequestFunc):
        """
        Process request middleware.

        Args:
            func (Callable): Function to be called before request.

        Example:

        ```python
        @app.middleware.process_request
        def process_request(request):
            print("Processing request")
            auth = request.headers.get("Authorization")
            if auth is None:
                raise HTTPException(status_code=401)
        ```

        """
        self.app.add_middleware(BaseMiddleware, process_request=func)
        return func

    def process_response(self, func: ProcessResponseFunc):
        """
        Process response middleware.

        Args:
            func (Callable): Function to be called after request.

        Example:

        ```python
        @app.middleware.process_response
        def process_response(response, exc):
            print("Processing response")
            success = "1" if exc is None else "0"
            response.headers["X-Success"] = success
        ```
        """
        self.app.add_middleware(BaseMiddleware, process_response=func)
        return func

    def process_websocket(self, func: ProcessWebSocketFunc):
        """
        Process websocket middleware.

        :param func: Function to be called before the request to WebSocket.

        Example:

        ```python
        @app.middleware.process_websocket
        def process_websocket(websocket):
            print("Processing websocket")
            # websocket.accept()
        ```
        """
        self.app.add_middleware(BaseMiddleware, process_websocket=func)
        return func

    def __call__(self, middleware_type: str):
        assert middleware_type in (
            "request",
            "response",
            "websocket",
        ), "middleware_type must be 'request', 'response or 'websocket'"
        func = getattr(self, "process_{}".format(middleware_type))
        return func
