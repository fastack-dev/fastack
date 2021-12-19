import os
import subprocess
from typing import Any, Callable, Dict, Optional, Type, Union

import click
from pkg_resources import get_distribution, iter_entry_points
from typer import Argument, Context, Exit, Option, Typer, colors, echo
from typer.main import get_group_name
from typer.models import Default

from . import generator
from .app import Fastack
from .utils import import_attr


class Command(Typer):
    def __init__(
        self,
        *,
        name: Optional[str] = Default(None),
        cls: Optional[Type[click.Command]] = Default(None),
        # invoke_without_command: bool = Default(False),
        # no_args_is_help: Optional[bool] = Default(None),
        subcommand_metavar: Optional[str] = Default(None),
        chain: bool = Default(False),
        result_callback: Optional[Callable[..., Any]] = Default(None),
        # Command
        context_settings: Optional[Dict[Any, Any]] = Default(None),
        # callback: Optional[Callable[..., Any]] = Default(None),
        help: Optional[str] = Default(None),
        epilog: Optional[str] = Default(None),
        short_help: Optional[str] = Default(None),
        options_metavar: str = Default("[OPTIONS]"),
        add_help_option: bool = Default(True),
        hidden: bool = Default(False),
        deprecated: bool = Default(False),
        add_completion: bool = True,
    ):
        no_args_is_help = invoke_without_command = True
        callback = self.init
        super().__init__(
            name=name,
            cls=cls,
            invoke_without_command=invoke_without_command,
            no_args_is_help=no_args_is_help,
            subcommand_metavar=subcommand_metavar,
            chain=chain,
            result_callback=result_callback,
            context_settings=context_settings,
            callback=callback,
            help=help,
            epilog=epilog,
            short_help=short_help,
            options_metavar=options_metavar,
            add_help_option=add_help_option,
            hidden=hidden,
            deprecated=deprecated,
            add_completion=add_completion,
        )
        self.load_commands()

    def init(
        self,
        ctx: Context,
        version: Optional[bool] = Option(
            None, "-v", "--version", is_eager=True, help="Show version number and exit"
        ),
    ):
        if ctx.resilient_parsing:  # pragma: no cover
            return

        if version:
            v = get_distribution("fastack").version
            echo(f"fastack v{v}")
            raise Exit

    def load_app(self) -> Union[Fastack, None]:
        os.chdir(os.getcwd())
        try:
            src = os.environ.get("FASTACK_APP", "app.main.app")
            app: Fastack = import_attr(src)
            if not isinstance(app, Fastack):
                echo(f"Invalid application type {app!r}")

            return app
        except (ImportError, AttributeError):
            pass

    def load_commands(self):
        for ep in iter_entry_points("fastack.commands"):  # pragma: no cover
            cmd = ep.load()
            if isinstance(cmd, Typer):
                self.add_typer(cmd)
            else:
                self.command(ep.name)(cmd)

        self.app = self.load_app()
        if self.app is not None:
            self.merge(self.app.cli)

    def merge(self, cli: Typer):
        for cmd in cli.registered_commands:
            found = False
            for idx, old in enumerate(self.registered_commands):
                old_name = old.name or old.callback.__name__
                cmd_name = cmd.name or cmd.callback.__name__
                if old_name == cmd_name:
                    self.registered_commands[idx] = cmd
                    found = True
                    break

            if not found:
                self.registered_commands.append(cmd)

        for group in cli.registered_groups:
            group_name = get_group_name(group) or group.name
            if group_name is None:
                continue

            found = False
            for idx, old in enumerate(self.registered_groups):
                old_name = get_group_name(old) or group.name
                if old_name == group_name:
                    self.registered_groups[idx] = group
                    found = True
                    break

            if not found:
                self.registered_groups.append(group)


fastack = Command(
    name="fastack",
    help="""
    fastack - blah blah blah framework!
    """,
    epilog="""
    fastack (c) 2021 aprila hijriyan.
    """,
)


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
