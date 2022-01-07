from fastack import Fastack
from fastack.globals import LocalProxy, state

say_hello: bool = LocalProxy(lambda: getattr(state, "say_hello", False))


def setup(app: Fastack):
    def on_startup():
        app.state.say_hello = True

    def on_shutdown():
        app.state.say_hello = False

    app.add_event_handler("startup", on_startup)
    app.add_event_handler("shutdown", on_shutdown)
