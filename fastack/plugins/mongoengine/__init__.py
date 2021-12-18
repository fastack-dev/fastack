from mongoengine import connect, disconnect_all

from fastack import Fastack


def setup(app: Fastack):
    @app.on_event("startup")
    def on_startup():
        url = f"mongodb+srv://{app.state.settings.MONGODB_USER}:{app.state.settings.MONGODB_PASSWORD}@{app.state.settings.MONGODB_HOST}/{app.state.settings.MONGODB_NAME}"
        connect(host=url)

    @app.on_event("shutdown")
    def on_shutdown():
        disconnect_all()
