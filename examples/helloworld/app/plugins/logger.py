import logging
import sys

from fastack import Fastack
from fastack.globals import LocalProxy, state

log: logging.Logger = LocalProxy(lambda: state.log)


def setup(app: Fastack):
    def on_startup():
        log = logging.getLogger("fastack_logger")
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        log.addHandler(handler)
        if app.debug:
            log.setLevel(logging.DEBUG)

        app.state.log = log
        log.info("Fastack logger initialized")

    def on_shutdown():
        log.info("Fastack logger cleanup")
        del app.state.log

    app.add_event_handler("startup", on_startup)
    app.add_event_handler("shutdown", on_shutdown)
