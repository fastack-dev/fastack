from typing import Any

from typer import Context, Typer, echo

from fastack import Fastack
from fastack.decorators import enable_context, with_asgi_lifespan

sub_cmd = Typer(name="sub", help="sub_cmd help")


@sub_cmd.command()
@with_asgi_lifespan
def foo(ctx: Context):
    """foo"""
    echo("foo 321")


def initializer(app: Fastack):
    echo("initializer")


def finalizer(app: Fastack, rv: Any):
    echo("finalizer")


@enable_context(initializer, finalizer)
async def bar():
    """bar"""

    echo("bar 123")
