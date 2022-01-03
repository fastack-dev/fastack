from types import ModuleType
from typing import Any, Callable, Coroutine, Dict, List, Optional, Sequence, Type, Union

from fastapi import Depends, FastAPI, Request, params, routing
from fastapi.datastructures import Default
from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRoute
from starlette.middleware import Middleware
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


def create_app(
    settings: ModuleType,
    routes: Optional[List[BaseRoute]] = None,
    title: str = "Fastack",
    description: str = "Fastack Framework",
    version: str = "0.1.0",
    openapi_url: Optional[str] = "/openapi.json",
    openapi_tags: Optional[List[Dict[str, Any]]] = None,
    servers: Optional[List[Dict[str, Union[str, Any]]]] = None,
    dependencies: Optional[Sequence[Depends]] = None,
    default_response_class: Type[Response] = Default(JSONResponse),
    docs_url: Optional[str] = "/docs",
    redoc_url: Optional[str] = "/redoc",
    swagger_ui_oauth2_redirect_url: Optional[str] = "/docs/oauth2-redirect",
    swagger_ui_init_oauth: Optional[Dict[str, Any]] = None,
    middleware: Optional[Sequence[Middleware]] = None,
    exception_handlers: Optional[
        Dict[
            Union[int, Type[Exception]],
            Callable[[Request, Any], Coroutine[Any, Any, Response]],
        ]
    ] = None,
    on_startup: Optional[Sequence[Callable[[], Any]]] = None,
    on_shutdown: Optional[Sequence[Callable[[], Any]]] = None,
    terms_of_service: Optional[str] = None,
    contact: Optional[Dict[str, Union[str, Any]]] = None,
    license_info: Optional[Dict[str, Union[str, Any]]] = None,
    openapi_prefix: str = "",
    root_path: str = "",
    root_path_in_servers: bool = True,
    responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
    callbacks: Optional[List[BaseRoute]] = None,
    deprecated: Optional[bool] = None,
    include_in_schema: bool = True,
    **extra: Any,
):
    if not contact:
        contact = {
            "name": "Fastack",
            "url": "https://github.com/fastack-dev/fastack",
        }

    app = Fastack(
        debug=settings.DEBUG,
        routes=routes,
        title=title,
        description=description,
        version=version,
        openapi_url=openapi_url,
        openapi_tags=openapi_tags,
        servers=servers,
        dependencies=dependencies,
        default_response_class=default_response_class,
        docs_url=docs_url,
        redoc_url=redoc_url,
        swagger_ui_oauth2_redirect_url=swagger_ui_oauth2_redirect_url,
        swagger_ui_init_oauth=swagger_ui_init_oauth,
        middleware=middleware,
        exception_handlers=exception_handlers,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        terms_of_service=terms_of_service,
        contact=contact,
        license_info=license_info,
        openapi_prefix=openapi_prefix,
        root_path=root_path,
        root_path_in_servers=root_path_in_servers,
        responses=responses,
        callbacks=callbacks,
        deprecated=deprecated,
        include_in_schema=include_in_schema,
        **extra,
    )
    app.add_middleware(MergeAppStateMiddleware)
    app.set_settings(settings)
    app.load_plugins()
    app.load_commands()
    return app
