import os
import sys
from importlib import import_module
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Type, Union

from fastapi.routing import APIRoute

if TYPE_CHECKING:
    from .app import Fastack  # pragma: no cover

from urllib.parse import urlencode, urlparse, urlunparse

from .globals import request


def import_attr(module: str) -> Any:
    """
    Import attributes from a module.

    Args:
        module: Module name (e.g. "os.path")

    Returns:
        Any: Imported attributes
    """

    package, attr = module.rsplit(".", 1)
    mod = import_module(package)
    return getattr(mod, attr)


def load_app(raise_error: bool = True) -> "Fastack":
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
        if raise_error:
            infoMsg = '\n  If you use the "fastack" command, you need to be in the root of the project directory '
            infoMsg += "or set the location of the app via the environment:\n"
            infoMsg += "    $ export FASTACK_APP=app.main.app\n"
            infoMsg += "    $ fastack runserver\n\n"
            infoMsg += "  I hope this helps!"
            raise RuntimeError(infoMsg) from e


def lookup_exception_handler(
    exception_handlers: Dict[Union[int, Type[Exception]], Callable],
    exc_or_status: Union[Exception, int],
) -> Optional[Callable]:
    """
    Lookup exception handler.
    Taken from starlette.exceptions.ExceptionMiddleware.
    """

    handler = None
    if isinstance(exc_or_status, Exception):
        for cls in type(exc_or_status).__mro__:
            if cls in exception_handlers:
                handler = exception_handlers[cls]
                break
    else:
        handler = exception_handlers.get(exc_or_status)

    return handler


def url_for(name: str, **params: Dict[str, Any]) -> str:
    """
    Generate absolute URL for an endpoint.

    Args:
        name: Name of the endpoint.
        params: Can be path parameters or query parameters.
    """

    path_params = {}
    routes: List[APIRoute] = request.app.routes
    for route in routes:
        if route.name == name:
            paths = list(route.param_convertors.keys())
            for path in paths:
                if path in params:
                    path_value = params.pop(path)
                    path_params[path] = path_value
            break

    url = request.url_for(name, **path_params)
    parsed = list(urlparse(url))
    query = urlencode(params, doseq=True)
    parsed[4] = query
    return urlunparse(parsed)
