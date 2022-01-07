import os
import sys
from importlib import import_module
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .app import Fastack


def import_attr(module: str) -> Any:
    """
    Import attributes from a module.

    :param module: Module name (e.g. "os.path")

    :return: Imported attributes
    """

    package, attr = module.rsplit(".", 1)
    module = import_module(package)
    return getattr(module, attr)


def load_app() -> "Fastack":
    """
    Load Fastack app from environment variable ``FASTACK_APP``.
    """

    cwd = os.getcwd()
    sys.path.insert(0, cwd)
    try:
        src = os.environ.get("FASTACK_APP", "app.main.app")
        app: "Fastack" = import_attr(src)
        return app

    except (ImportError, AttributeError) as e:
        infoMsg = '\n  If you use the "fastack" command, you need to be in the root of the project directory '
        infoMsg += "or set the location of the app via the environment:\n"
        infoMsg += "    $ export FASTACK_APP=app.main.app\n"
        infoMsg += "    $ fastack runserver\n\n"
        infoMsg += "  I hope this helps!"
        raise RuntimeError(infoMsg) from e
