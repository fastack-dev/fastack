import asyncio
import warnings
from functools import wraps
from inspect import iscoroutinefunction
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Type, Union

import anyio
import click
from asgi_lifespan import LifespanManager
from fastapi import APIRouter, Response, params
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.encoders import DictIntStrAny, SetIntStr
from fastapi.responses import JSONResponse
from starlette.routing import BaseRoute
from starlette.types import ASGIApp

from .context import _app_ctx_stack
from .utils import load_app


def with_asgi_lifespan(func: Callable[..., Any]) -> Callable[..., Any]:
    warnings.warn(
        "with_asgi_lifespan is deprecated, use enable_context instead",
        DeprecationWarning,
        stacklevel=2,
    )

    @wraps(func)
    def executor(*args, **kwds):
        ctx = None
        for _, v in kwds.items():
            if isinstance(v, click.core.Context):
                ctx = v
                break

        assert isinstance(
            ctx, click.core.Context
        ), "with_asgi_lifespan decorator requires a context"
        app = ctx.obj

        async def wrapper() -> Any:
            try:
                async with LifespanManager(app):
                    _app_ctx_stack.push(app)
                    if iscoroutinefunction(func):
                        return await func(*args, **kwds)
                    return func(*args, **kwds)
            finally:
                _app_ctx_stack.pop()

        return anyio.run(wrapper)

    return executor


def enable_context(
    initializer: Callable = None, finalizer: Callable = None
) -> Callable:
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            ctx = None
            for _, v in kwargs.items():
                if isinstance(v, click.core.Context):
                    ctx = v
                    break

            app: ASGIApp = load_app()
            if ctx:
                ctx.obj = app

            async def executor():
                try:
                    if callable(initializer):
                        initializer(app)

                    async with LifespanManager(app):
                        _app_ctx_stack.push(app)
                        if iscoroutinefunction(func):
                            rv = await func(*args, **kwargs)
                        else:
                            rv = func(*args, **kwargs)

                        if callable(finalizer):
                            finalizer(app, rv)

                        return rv
                finally:
                    _app_ctx_stack.pop()

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
    openapi_extra: Optional[Dict[str, Any]] = None
):
    def wrapper(func):
        if iscoroutinefunction(func):

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
