from fastack import Fastack
from fastack.globals import LocalProxy, state

say_hello: bool = LocalProxy(lambda: getattr(state, "say_hello", False))


def setup(app: Fastack):
    app.state.say_hello = True
