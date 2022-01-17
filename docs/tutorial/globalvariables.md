# Global Variables

aims to make all objects globally accessible and make it easy for us to use them without passing function arguments. We provide global variables to access:

* [Current App](#application)
* [State](#state)
* [Request Object](#request)
* [Websocket Object](#websocket)

!!! note

    All global objects are stored in `fastack.globals`.

## Application

You can access the app object via the ``current_app`` variable. For example:

```py title="app/controllers/config.py"
from fastack import Controller
from fastack.globals import current_app

class ConfigController(Controller):
    def get(self, name: str):
        return self.json("Config", {"setting": name, "value": current_app.get_setting(name)})
```

Add the above controller into the app and if you send

```
curl -X 'GET' \
   'http://127.0.0.1:7874/config?name=DEBUG' \
   -H 'accept: application/json'
```

you will get

```json
{
  "detail": "Config",
  "data": {
    "setting": "DEBUG",
    "value": true
  }
}
```

!!! warning

    Never add controller above, it's dangerous because it will know the settings used by your application!

!!! note

    `current_app` can be used if:

    * Already running the app. Or...
    * Using `enable_context()` decorator.

## State

``fastack.globals.state`` here is a shortcut for ``current_app.state`` which is used to access the plugins in it. [See here](./plugins.md) for more details.

## Request

Now you no longer need to use the `request` object on a responder, because we have set it up globally and you can access it anywhere 🥳

For example:

```py title="app/controllers/helloworld/__init__.py" linenums="1" hl_lines="9 27 36"
--8<-- "examples/helloworld/app/controllers/helloworld/__init__.py"
```

Line:

* `9` - We import the global `request` object
* `27` and `36` - We use the `url_for` method in the `request` object to generate absolute url.

## WebSocket

You can also access websocket connections globally via `fastack.globals.websocket`.

!!! warning "Technical details"

    Keep in mind, when you use websocket connection from ``fastack.globals.websocket`` you should not use `websocket` from typing hint in responder. This will cause the connection between the client and server to be out of sync.

    For example:

    ```py
    from fastapi import WebSocket

    @app.middleware("websocket")
    async def on_websocket(ws: WebSocket):
      ws.accept()

    @app.websocket("/ws")
    async def hello_ws(websocket: WebSocket):
        await websocket.send_json({"hello": "world"})
        await websocket.close()
    ```

    When you send data to client using websocket object from typing hint, it won't work because in websocket middleware *we allow all incoming connections* and *use websocket object from global*, while *websocket from typing hint in responder connection status is still not connected* (out of sync with global object)

    The example below should work fine.

    ```py
    from fastapi import WebSocket
    from fastack.globals import websocket

    @app.middleware("websocket")
    async def on_websocket(ws: WebSocket):
      ws.accept()

    @app.websocket("/ws")
    async def hello_ws(): # (1)
        await websocket.send_json({"hello": "world"})
        await websocket.close()
    ```

    1. We remove the websocket argument and use websocket from global

## How it works?

First, thanks to [werkzeug.local](https://werkzeug.palletsprojects.com/en/2.0.x/local/) for providing an API for object proxying.

It's simpler than you think (maybe :D). Basically a web framework is an object that can be called and accept requests that are forwarded by the web server.

This is the main point, we save the app instance to local context using API from `contextvars.ContextVar` and also `werkzeug.local.LocalProxy` to access objects stored in local context.

For more details, please see the documentation directly:

* [werkzeug.local](https://werkzeug.palletsprojects.com/en/2.0.x/local/)
* [contextvars](https://docs.python.org/3/library/contextvars.html)
