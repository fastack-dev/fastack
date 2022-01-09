import asyncio
from typing import Union

import anyio
from fastapi import FastAPI, HTTPException
from starlette.concurrency import run_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import Receive, Scope, Send
from starlette.websockets import WebSocket

from .globals import request, websocket
from .utils import lookup_exception_handler


class BaseMiddleware(BaseHTTPMiddleware):
    """
    Middleware that supports HTTP and WebSocket connections
    """

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        scope_type = scope["type"]
        if scope_type == "http":
            try:
                await self.process_request(request)
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

                    await self.process_response(response, exc)
                    await response(scope, receive, send)
                    task_group.cancel_scope.cancel()
                    return

        elif scope_type == "websocket":
            await self.process_websocket(websocket)

        return await super().__call__(scope, receive, send)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        await self.process_response(response)
        return response

    async def process_request(self, request: Request):
        """
        Process the http request
        """
        raise NotImplementedError

    async def process_response(self, response: Response, exc: HTTPException = None):
        """
        Process the response

        :param response: The response object
        :param exc: The exception object if error occured
        """

    async def process_websocket(self, websocket: WebSocket):
        """
        Process the websocket.
        This is similar to process_request but for websocket.
        """

        raise NotImplementedError

    async def process_exception(self, request: Request, exc: Exception) -> Response:
        """
        Process the exception.
        """
        raise exc


class MergeAppStateMiddleware(BaseMiddleware):
    """
    Middleware that combines state in application to request and websocket.
    """

    def update_state(self, object: Union[Request, WebSocket]):
        object.state._state.update(object.app.state._state)

    async def process_request(self, request: Request):
        self.update_state(request)

    async def process_websocket(self, websocket: WebSocket):
        self.update_state(websocket)
