from app import models, settings  # noqa
from app.controllers import init_controllers

from fastack import create_app

app = create_app(settings)
init_controllers(app)
