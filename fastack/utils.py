import os
import sys
from importlib import import_module
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .app import Fastack


def import_attr(module: str):
    package, attr = module.rsplit(".", 1)
    module = import_module(package)
    return getattr(module, attr)


def load_app() -> Union["Fastack", None]:
    cwd = os.getcwd()
    sys.path.insert(0, cwd)
    try:
        src = os.environ.get("FASTACK_APP", "app.main.app")
        app: "Fastack" = import_attr(src)
        return app

    except (ImportError, AttributeError):
        pass
