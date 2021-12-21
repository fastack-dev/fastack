from functools import wraps
from inspect import iscoroutinefunction
from typing import Any, Callable

import anyio
import click
from asgi_lifespan import LifespanManager


def with_asgi_lifespan(func: Callable[..., Any]) -> Callable[..., Any]:
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
            async with LifespanManager(app):
                if iscoroutinefunction(func):
                    return await func(*args, **kwds)
                return func(*args, **kwds)

        return anyio.run(wrapper)

    return executor


def route(**params):
    def wrapper(func):
        if iscoroutinefunction(func):

            @wraps(func)
            async def decorated(*args, **kwds):
                return await func(*args, **kwds)

        else:

            @wraps(func)
            def decorated(*args, **kwds):
                return func(*args, **kwds)

        decorated.__route_params__ = params
        return decorated

    return wrapper
