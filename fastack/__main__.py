import uvicorn
from cookiecutter.main import cookiecutter
from typer import Argument, Context, Option, echo

from .app import Fastack
from .cli import Command

fastack = Command(
    name="fastack",
    help="""
    fastack is an intuitive framework based on FastAPI.
    """,
    epilog="""
    fastack (c) 2021 aprila hijriyan.
    """,
)


@fastack.command()
def runserver(ctx: Context):
    """
    Run app with uvicorn.
    """

    app = ctx.obj
    if not isinstance(app, Fastack):
        echo(f"Invalid application type {app!r}")
        ctx.exit(1)

    uvicorn.run(ctx.obj)


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
