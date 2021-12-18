from functools import wraps
from inspect import iscoroutinefunction


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
