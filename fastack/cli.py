import subprocess

from pkg_resources import iter_entry_points
from typer import Argument, Context, Typer, colors, echo
from typer.main import get_group_name

from . import generator
from .app import Fastack
from .utils import import_attr

fastack = Typer(
    name="fastack",
    help="""
    fastack - blah blah blah framework!
    """,
    epilog="""
    fastack (c) 2021 aprila hijriyan.
    """,
)


@fastack.callback()
def init():
    for ep in iter_entry_points("fastack.commands"):  # pragma: no cover
        cmd = ep.load()
        if isinstance(cmd, Typer):
            fastack.add_typer(cmd)
        else:
            fastack.command(ep.name)(cmd)

    try:
        app: Fastack = import_attr("app.main.app")
    except (ImportError, AttributeError):
        return

    self = fastack
    for cmd in app.cli.registered_commands:
        for idx, old in enumerate(self.registered_commands):
            old_name = old.name or old.callback.__name__
            cmd_name = cmd.name or cmd.callback.__name__
            if old_name == cmd_name:
                self.registered_commands[idx] = cmd
                break

    for group in app.cli.registered_groups:
        group_name = get_group_name(group)
        if group_name is None:
            continue

        for idx, old in enumerate(self.registered_groups):
            old_name = get_group_name(old)
            if old_name == group_name:
                self.registered_groups[idx] = group
                break


@fastack.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def runserver(ctx: Context):
    """
    Run app with uvicorn.
    """

    subprocess.call(["uvicorn", "app.main:app"] + ctx.args)


@fastack.command()
def new(name: str = Argument(..., help="Project name")):
    """
    Create project.
    """

    echo(f"Creating project: {name}...", color=colors.BRIGHT_GREEN)
    generator.create_project(name)
