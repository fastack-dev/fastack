from mongoengine import connect, disconnect_all

from fastack import Fastack


def setup(app: Fastack):
    @app.on_event("startup")
    def on_startup():
        url = app.state.settings.MONGODB_URI
        connect(host=url)

    @app.on_event("shutdown")
    def on_shutdown():
        disconnect_all()
