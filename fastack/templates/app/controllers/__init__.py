from app.controllers.dummy import DummyController

from fastack import Fastack


def init_controllers(app: Fastack):
    app.include_controller(DummyController())
