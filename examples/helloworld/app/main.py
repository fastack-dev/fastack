from app import models, settings  # noqa
from app.controllers import init_controllers

from fastack import create_app
from fastack.globals import websocket

app = create_app(settings)
init_controllers(app)


@app.websocket("/ws")
async def ws():
    await websocket.accept()
    await websocket.send_json({"hi": "there!"})
