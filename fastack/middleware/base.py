import asyncio
from typing import Awaitable, Callable, Optional

import anyio
from fastapi import FastAPI, HTTPException
from starlette.concurrency import run_in_threadpool
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    DispatchFunction,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.websockets import WebSocket

from ..globals import request, websocket
from ..utils import lookup_exception_handler

ProcessRequestFunc = Callable[[Request], Awaitable[None]]
ProcessResponseFunc = Callable[[Response, Optional[Exception]], Awaitable[None]]
ProcessWebSocketFunc = Callable[[WebSocket], Awaitable[None]]


class BaseMiddleware(BaseHTTPMiddleware):
    """
    Middleware that supports HTTP and WebSocket connections
    """

    def __init__(
        self,
        app: ASGIApp,
        *,
        dispatch: Optional[DispatchFunction] = None,
        process_request: Optional[ProcessRequestFunc] = None,
        process_response: Optional[ProcessResponseFunc] = None,
        process_websocket: Optional[ProcessWebSocketFunc] = None,
    ) -> None:
        self.app = app
        self.dispatch_func = self.dispatch if dispatch is None else dispatch
        self.process_request_func = (
            self.process_request if process_request is None else process_request
        )
        self.process_response_func = (
            self.process_response if process_response is None else process_response
        )
        self.process_websocket_func = (
            self.process_websocket if process_websocket is None else process_websocket
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        scope_type = scope["type"]
        if scope_type == "http":
            try:
                await self.process_request_func(request)
            except Exception as exc:
                async with anyio.create_task_group() as task_group:
                    app: FastAPI = request.app
                    exception_handlers = app.exception_handlers
                    handler = None
                    if isinstance(exc, HTTPException):
                        handler = lookup_exception_handler(
                            exception_handlers, exc.status_code
                        )

                    if handler is None:
                        handler = lookup_exception_handler(exception_handlers, exc)

                    if handler is None:
                        raise

                    if asyncio.iscoroutinefunction(handler):
                        response = await handler(request, exc)
                    else:
                        response = await run_in_threadpool(handler, request, exc)

                    await self.process_response_func(response, exc)  # type: ignore[operator]
                    await response(scope, receive, send)
                    task_group.cancel_scope.cancel()
                    return

        elif scope_type == "websocket":
            await self.process_websocket_func(websocket)

        return await super().__call__(scope, receive, send)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        await self.process_response_func(response)  # type: ignore[operator]
        return response

    async def process_request(self, request: Request):
        """
        Process the http request
        """

    async def process_response(
        self, response: Response, exc: Optional[Exception] = None
    ):
        """
        Process the response

        Args:
            response: The response object
            exc: The exception object if error occured

        Notes:
            The exception is always ``None`` when you use functions as middleware.
        """

    async def process_websocket(self, websocket: WebSocket):
        """
        Process the websocket.
        This is similar to process_request but for websocket.
        """
