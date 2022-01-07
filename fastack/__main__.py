import nest_asyncio

nest_asyncio.apply()

import uvicorn
from cookiecutter.main import cookiecutter
from typer import Argument, Option

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
@enable_context()
def runserver(port: int = Option(6000, "-p", "--port", help="Port to run the server.")):
    """
    Run app with uvicorn.
    """

    app = current_app._get_current_object()
    uvicorn.run(app, port=port, lifespan="on")


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


if __name__ == "__main__":
    fastack()
