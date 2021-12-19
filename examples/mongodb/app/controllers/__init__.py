from app.controllers.book import BookController

from fastack import Fastack


def init_controllers(app: Fastack):
    app.include_controller(BookController())
