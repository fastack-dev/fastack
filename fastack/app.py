from types import ModuleType
from typing import Any

from fastapi import FastAPI
from typer import Typer

from fastack.controller import Controller

from .utils import import_attr


class Fastack(FastAPI):
    cli = Typer()

    def set_settings(self, settings: ModuleType):
        self.state.settings = settings

    def get_setting(self, name: str, default: Any = None):
        assert self.state.settings is not None
        return getattr(self.state.settings, name, default)

    def load_plugins(self):
        for plugin in self.get_setting("PLUGINS", []):
            plugin += ".setup"
            plugin = import_attr(plugin)
            plugin(self)

    def load_commands(self):
        for command in self.get_setting("COMMANDS", []):
            command = import_attr(command)
            self.cli.add_typer(command)

    def include_controller(self, controller: Controller, **kwds):
        router = controller.build(**kwds)
        self.include_router(router)


def create_app(settings: ModuleType, **kwds):
    kwds["debug"] = settings.DEBUG
    app = Fastack(**kwds)
    app.set_settings(settings)
    app.load_plugins()
    app.load_commands()
    return app
