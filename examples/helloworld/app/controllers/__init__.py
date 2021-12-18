from app.controllers.helloworld import HelloWorldController

from fastack import Fastack


def init_controllers(app: Fastack):
    app.include_controller(HelloWorldController())
