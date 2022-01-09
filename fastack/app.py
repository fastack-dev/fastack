from types import ModuleType
from typing import Any, Callable, Coroutine, Dict, List, Optional, Sequence, Type, Union

from fastapi import Depends, FastAPI, Request, WebSocket, params, routing
from fastapi.datastructures import Default
from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRoute
from starlette.middleware import Middleware
from starlette.routing import BaseRoute
from starlette.types import ASGIApp, Receive, Scope, Send
from typer import Typer

from .context import _app_ctx_stack, _request_ctx_stack, _websocket_ctx_stack
from .controller import Controller
from .middleware import MiddlewareManager, StateMiddleware
from .utils import import_attr


class Fastack(FastAPI):
    """
    Fastack application aims to support:

    * App settings
    * Adding a plugin
    * Adding a command
    * Adding a controller to create a REST APIs
    * Access ``app``, ``request``, ``websocket``, ``state`` objects globally (like Flask)

    """

    # Storage for all commands and will be added to the "fastack" command, so you can access it.
    cli = Typer()

    def set_settings(self, settings: ModuleType):
        """
        Set settings for the application.

        :param settings: settings module
        """

        self.state.settings = settings

    def get_setting(self, name: str, default: Any = None):
        """
        Get setting value by name.

        Args:
            name (str): Setting name
            default (Any, optional): Default value if setting is not found. Defaults to None.

        Returns:
            Any: Setting value
        """

        assert self.state.settings is not None
        return getattr(self.state.settings, name, default)

    def load_plugins(self):
        """
        Load plugins from settings.
        """

        for plugin in self.get_setting("PLUGINS", []):
            plugin += ".setup"
            plugin = import_attr(plugin)
            plugin(self)

    def load_commands(self):
        """
        Load commands from settings.
        """

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
        """
        Include controller to the application.

        :param controller: Controller instance

        For other parameters, please see the documentation of ``fastapi.APIRouter.add_api_route``.
        """

        assert isinstance(
            controller, Controller
        ), f"Controller must be an instance of {Controller!r}"
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

    @property
    def middleware(self) -> MiddlewareManager:
        return MiddlewareManager(self)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        try:
            # Add the app instance to the global stack, so you can access it globally via ``fastack.globals.current_app``
            _app_ctx_stack.push(self)
            scope_type = scope["type"]
            # If the scope is http we will create a request instance object and add it to the global stack,
            # so that it can be accessed via ``fastack.globals.request``
            if scope_type == "http":
                request = Request(scope, receive)
                _request_ctx_stack.push(request)

            # Same as above, but for websocket
            elif scope_type == "websocket":
                websocket = WebSocket(scope, receive, send)
                _websocket_ctx_stack.push(websocket)

            await super().__call__(scope, receive, send)
        finally:
            # Clean global stack, when app finish processing request
            _websocket_ctx_stack.pop()
            _request_ctx_stack.pop()
            _app_ctx_stack.pop()


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
    """
    Create a Fastack application.
    """

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
    app.add_middleware(StateMiddleware)
    app.set_settings(settings)
    app.load_plugins()
    app.load_commands()
    return app
