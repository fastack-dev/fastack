from types import ModuleType
from typing import Any, Callable, Dict, List, Optional, Sequence, Type, Union

from fastapi import FastAPI, params, routing
from fastapi.datastructures import Default
from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRoute
from starlette.routing import BaseRoute
from starlette.types import ASGIApp
from typer import Typer

from .controller import Controller
from .middleware import MergeAppStateMiddleware
from .utils import import_attr


class Fastack(FastAPI):
    cli = Typer()

    def set_settings(self, settings: ModuleType):
        self.state.settings = settings

    def get_setting(self, name: str, default: Any = None):
        assert self.state.settings is not None
        return getattr(self.state.settings, name, default)

    def load_plugins(self):
        for plugin in self.get_setting("PLUGINS", []):
            plugin += ".setup"
            plugin = import_attr(plugin)
            plugin(self)

    def load_commands(self):
        for command in self.get_setting("COMMANDS", []):
            command: Union[Callable, Typer] = import_attr(command)
            if isinstance(command, Typer):
                self.cli.add_typer(command)
            else:
                self.cli.command(command.__name__)(command)

    def include_controller(
        self,
        controller: Controller,
        *,
        prefix: str = "",
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
        default_response_class: Type[Response] = Default(JSONResponse),
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        routes: Optional[List[routing.BaseRoute]] = None,
        redirect_slashes: bool = True,
        default: Optional[ASGIApp] = None,
        dependency_overrides_provider: Optional[Any] = None,
        route_class: Type[APIRoute] = APIRoute,
        on_startup: Optional[Sequence[Callable[[], Any]]] = None,
        on_shutdown: Optional[Sequence[Callable[[], Any]]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
    ):
        assert isinstance(
            controller, Controller
        ), f"Controller must be an instance of {controller!r}"
        router = controller.build(
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
            default_response_class=default_response_class,
            responses=responses,
            callbacks=callbacks,
            routes=routes,
            redirect_slashes=redirect_slashes,
            default=default,
            dependency_overrides_provider=dependency_overrides_provider,
            route_class=route_class,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
        )
        self.include_router(router)


def create_app(settings: ModuleType, **kwds):
    kwds.setdefault("title", "Fastack")
    kwds.setdefault("description", "Fastack Framework")
    kwds.setdefault(
        "contact",
        {
            "name": "Fastack",
            "url": "https://github.com/fastack-dev/fastack",
        },
    )
    kwds["debug"] = settings.DEBUG
    app = Fastack(**kwds)
    app.add_middleware(MergeAppStateMiddleware)
    app.set_settings(settings)
    app.load_plugins()
    app.load_commands()
    return app
