from app import models, settings  # noqa
from app.controllers import init_controllers
from app.plugins.globalvar import say_hello

from fastack import create_app
from fastack.globals import websocket

app = create_app(settings)
init_controllers(app)


@app.websocket("/ws")
async def ws():
    if say_hello:
        km = "beautiful girl"
    else:
        km = "cuk"

    await websocket.accept()
    await websocket.send_json({"hi": km})
