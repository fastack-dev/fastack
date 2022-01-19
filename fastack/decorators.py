import asyncio
import warnings
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Type, Union

import anyio
import click
from asgi_lifespan import LifespanManager
from fastapi import APIRouter, FastAPI, Response, params
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.encoders import DictIntStrAny, SetIntStr
from fastapi.responses import JSONResponse
from starlette.routing import BaseRoute
from starlette.types import ASGIApp
from typer.core import TyperCommand
from typer.models import CommandFunctionType, CommandInfo

from .context import _app_ctx_stack
from .utils import load_app


def with_asgi_lifespan(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def executor(*args, **kwds):
        warnings.warn(
            "with_asgi_lifespan is deprecated, use enable_context instead",
            DeprecationWarning,
            stacklevel=2,
        )
        ctx = None
        for _, v in kwds.items():
            if isinstance(v, click.core.Context):
                ctx = v
                break

        assert isinstance(
            ctx, click.core.Context
        ), "with_asgi_lifespan decorator requires a context"
        app = ctx.obj
        assert isinstance(app, FastAPI), "Invalid application type"

        async def wrapper() -> Any:
            token = None
            try:
                async with LifespanManager(app):
                    token = _app_ctx_stack.set(app)
                    if asyncio.iscoroutinefunction(func):
                        return await func(*args, **kwds)  # pragma: no cover
                    return func(*args, **kwds)
            finally:
                if token:
                    _app_ctx_stack.reset(token)

        return anyio.run(wrapper)

    return executor


def enable_context(
    initializer: Callable[[ASGIApp], Any] = None,
    finalizer: Callable[[ASGIApp, Any], Any] = None,
) -> Callable:
    """
    A decorator that activates the application context
    The function can be a coroutine or a normal function.

    Args:
        initializer: The function to be called before application context starts.
        finalizer: The function that will be called after your function is called.

    notes:
        - The initializer will accept one argument. ``initializer(app)`` where ``app`` is the application.
        - The finalizer will accept two argument. ``finalizer(app, rv)`` where ``app`` is the application and ``rv`` is the return value of the function.

    """

    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            ctx = None
            for _, v in kwargs.items():
                # Finding Context in parameters
                if isinstance(v, click.core.Context):  # pragma: no cover
                    ctx = v
                    break

            app: ASGIApp
            if ctx is None:
                app = load_app()
            else:
                # This is always a FastAPI object, below is just for checking.
                app = ctx.obj  # pragma: no cover
                if not isinstance(app, FastAPI):  # pragma: no cover
                    app = load_app()
                    ctx.obj = app

            assert isinstance(app, FastAPI), "Invalid application type"

            async def executor():
                token = None
                try:
                    if callable(initializer):
                        initializer(app)

                    async with LifespanManager(app):
                        token = _app_ctx_stack.set(app)
                        if asyncio.iscoroutinefunction(func):
                            rv = await func(*args, **kwargs)
                        else:
                            rv = func(*args, **kwargs)  # pragma: no cover

                        if callable(finalizer):
                            finalizer(app, rv)

                        return rv
                finally:
                    if token:
                        _app_ctx_stack.reset(token)

            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()

            task = loop.create_task(executor())
            return loop.run_until_complete(task)

        return decorator

    return wrapper


def route(
    path: Optional[str] = None,
    *,
    action: bool = False,
    response_model: Optional[Type[Any]] = None,
    status_code: Optional[int] = None,
    tags: Optional[List[str]] = None,
    dependencies: Optional[Sequence[params.Depends]] = None,
    summary: Optional[str] = None,
    description: Optional[str] = None,
    response_description: str = "Successful Response",
    responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
    deprecated: Optional[bool] = None,
    methods: Optional[Union[Set[str], List[str]]] = None,
    operation_id: Optional[str] = None,
    response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
    response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
    response_model_by_alias: bool = True,
    response_model_exclude_unset: bool = False,
    response_model_exclude_defaults: bool = False,
    response_model_exclude_none: bool = False,
    include_in_schema: bool = True,
    response_class: Union[Type[Response], DefaultPlaceholder] = Default(JSONResponse),
    name: Optional[str] = None,
    route_class_override: Optional[Type[APIRouter]] = None,
    callbacks: Optional[List[BaseRoute]] = None,
    openapi_extra: Optional[Dict[str, Any]] = None,
):
    """
    A decorator to add additional information for endpoints in OpenAPI.

    :param path: The path of the endpoint.
    :param action: To mark this method is the responder to be included in the controller.
    """

    def wrapper(func):
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def decorated(*args, **kwds):
                return await func(*args, **kwds)

        else:

            @wraps(func)
            def decorated(*args, **kwds):
                return func(*args, **kwds)

        params = getattr(decorated, "__route_params__", {})
        params.update(
            {
                "path": path,
                "response_model": response_model,
                "status_code": status_code,
                "tags": tags,
                "dependencies": dependencies,
                "summary": summary,
                "description": description,
                "response_description": response_description,
                "responses": responses,
                "deprecated": deprecated,
                "methods": methods,
                "operation_id": operation_id,
                "response_model_include": response_model_include,
                "response_model_exclude": response_model_exclude,
                "response_model_by_alias": response_model_by_alias,
                "response_model_exclude_unset": response_model_exclude_unset,
                "response_model_exclude_defaults": response_model_exclude_defaults,
                "response_model_exclude_none": response_model_exclude_none,
                "include_in_schema": include_in_schema,
                "response_class": response_class,
                "name": name,
                "route_class_override": route_class_override,
                "callbacks": callbacks,
                "openapi_extra": openapi_extra,
            }
        )
        decorated.__route_params__ = params
        decorated.__route_action__ = action
        return decorated

    return wrapper


def command(
    name: Optional[str] = None,
    *,
    cls: Optional[Type[click.Command]] = None,
    context_settings: Optional[Dict[Any, Any]] = None,
    help: Optional[str] = None,
    epilog: Optional[str] = None,
    short_help: Optional[str] = None,
    options_metavar: str = "[OPTIONS]",
    add_help_option: bool = True,
    no_args_is_help: bool = False,
    hidden: bool = False,
    deprecated: bool = False,
) -> Callable[[CommandFunctionType], CommandFunctionType]:
    if cls is None:
        cls = TyperCommand

    def decorator(f: CommandFunctionType) -> CommandFunctionType:
        # Inject command info here which will be used by fastack.cli.Command.merge
        f.__command_info__ = CommandInfo(
            name=name,
            cls=cls,
            context_settings=context_settings,
            callback=f,
            help=help,
            epilog=epilog,
            short_help=short_help,
            options_metavar=options_metavar,
            add_help_option=add_help_option,
            no_args_is_help=no_args_is_help,
            hidden=hidden,
            deprecated=deprecated,
        )
        return f

    return decorator
