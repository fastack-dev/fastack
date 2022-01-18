from typing import Any, Callable, Dict, Optional, Type, Union

import click
from pkg_resources import get_distribution, iter_entry_points
from typer import Context, Exit, Option, Typer, echo
from typer.models import CommandInfo, Default

from .app import Fastack
from .utils import load_app


class Command(Typer):
    """
    Command base for fastack cli
    """

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
        self.app: Union[Fastack, None] = load_app(raise_error=False)
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

        ctx.obj = self.app

        if version:
            v = get_distribution("fastack").version
            echo(f"fastack v{v}")
            raise Exit

    def load_commands(self):
        for ep in iter_entry_points("fastack.commands"):  # pragma: no cover
            cmd = ep.load()
            if isinstance(cmd, Typer):
                self.add_typer(cmd)
            else:
                self.merge_command(cmd, name=ep.name)

        if self.app is not None:
            self.merge(self.app.cli)

    def merge_command(self, command: Union[Callable, CommandInfo], *, name: str = None):
        if isinstance(command, CommandInfo):
            cmd_name = name or command.name
            command_info = command
        else:
            cmd_name = name or command.__name__
            command_info: Optional[CommandInfo] = getattr(
                command, "__command_info__", None
            )
            if command_info is None:
                command_info = CommandInfo(
                    name=cmd_name,
                    callback=command,
                )
            else:
                cmd_name = name or command_info.name or command.__name__

        if not isinstance(command_info, CommandInfo):  # pragma: no cover
            raise TypeError(f"Invalid command info type on {command!r}")

        found = False
        for idx, old in enumerate(self.registered_commands):
            old_name = old.name
            if not old_name:
                old_name = old.callback.__name__

            if old_name and old_name == cmd_name:
                self.registered_commands[idx] = command_info
                found = True
                break

        if not found:
            self.registered_commands.append(command_info)

    def merge_typer(self, typer: Typer):
        for group in typer.registered_groups:
            group_name = group.typer_instance.info.name
            if not group_name:
                continue  # pragma: no cover

            found = False
            for idx, old in enumerate(self.registered_groups):
                old_name = old.typer_instance.info.name
                if old_name and old_name == group_name:
                    self.registered_groups[idx] = group
                    found = True
                    break

            if not found:
                self.registered_groups.append(group)

    def merge(self, cli: Union[Typer, Callable]):
        if isinstance(cli, Typer):
            self.merge_typer(cli)
            for command in cli.registered_commands:
                self.merge_command(command)
        else:
            self.merge_command(cli)
