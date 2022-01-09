# Middleware

Our middleware supports HTTP and WebSocket connections in one middleware, also supports exception handling in the middleware.

## Create middleware

There are two ways to create middleware.

1. With class ``fastack.middleware.base.BaseMiddleware``
2. With middleware manager ``fastack.app.Fastack.middleware``

### Middleware with class

```python
from fastapi import HTTPException, Request, Response, WebSocket, status

from fastack.middleware.base import BaseMiddleware

class AuthMiddleware(BaseMiddleware):
    async def process_request(self, request: Request):
        auth = request.headers.get("Authorization")
        if auth != "Bearer test":
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized")

    async def process_response(self, response: Response, exc: Exception = None):
        response.headers["X-Success"] = "1" if response.status_code == 404 else "0"

    async def process_websocket(self, websocket: WebSocket):
        # accept all incoming connections
        await websocket.accept()
```

Add middleware to application:

```python
app.add_middleware(AuthMiddleware)
```

Explanation of the `process_*` method:

* ``process_request`` - Function to handle HTTP requests prior to controller.
* ``process_response`` - Function to handle response after processing from controller or received exception thrown by ``process_request``
* ``process_websocket`` - Function to handle websocket connection request prior to endpoint.


### Middleware with manager

```python
from fastapi import HTTPException, Request, Response, WebSocket, status

@app.middleware("request")
async def on_request(request: Request):
    auth = request.headers.get("Authorization")
    if auth != "Bearer test":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized")

@app.middleware("response")
async def on_response(response: Response, exc: Exception = None):
    response.headers["X-Success"] = "1" if response.status_code == 404 else "0"

@app.middleware("websocket")
async def on_websocket(ws: WebSocket):
    await ws.accept()
```

??? info "About `#!python @app.middleware("request")`"

    This is a shortcut for the ``process_request`` method

??? info "About `#!python @app.middleware("response")`"

    This is a shortcut for the ``process_response`` method

??? info "About `#!python @app.middleware("websocket")`"

    This is a shortcut for the ``process_websocket`` method

!!! notes "For FastAPI users"

    It's compatible with `#!python FastAPI.middleware`, so don't worry ^^
