from typing import List, Union

import uvicorn  # type: ignore[import]
from cookiecutter.main import cookiecutter  # type: ignore[import]
from fastapi.routing import APIRoute, APIWebSocketRoute
from typer import Argument, Context, Option, echo

from .cli import Command
from .decorators import enable_context
from .globals import current_app

fastack = Command(
    name="fastack",
    help="""
    fastack is an intuitive framework based on FastAPI.
    """,
    epilog="""
    fastack (c) 2021 - 2022 aprila hijriyan.
    """,
)


@fastack.command()
def runserver(
    ctx: Context,
    port: int = Option(2304, "-p", "--port", help="Port to run the server."),
):
    """
    Run app with uvicorn.
    """

    app = ctx.obj
    if not app:
        echo("Can't find app")
        ctx.exit()

    uvicorn.run(app, port=port, lifespan="on", debug=True)  # pragma: no cover


@fastack.command()
def new(
    name: str = Argument(None, help="Project name"),
    output_dir: str = Argument(".", help="Output Directory"),
    template: str = Option(
        "gh:fastack-dev/fastack-app-starter-kit",
        "-t",
        "--template",
        help="Cookiecutter Template",
    ),
):
    """
    Create project.
    """

    extra_context = {}
    if name:
        extra_context["project_name"] = name

    cookiecutter(template, output_dir=output_dir, extra_context=extra_context)


@fastack.command()
@enable_context()
def routes():
    """
    List all routes.
    """

    echo("List of all routes:")
    routes: List[Union[APIRoute, APIWebSocketRoute]] = current_app.routes
    for route in routes:
        path_str = f"* {route.path}"
        if isinstance(route, APIRoute):
            path_str += f" {route.methods!r}"
        path_str += f" ({route.name})"
        print(path_str)


if __name__ == "__main__":
    fastack()  # pragma: no cover
