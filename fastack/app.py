from types import ModuleType
from typing import Any, Callable, Union

from fastapi import FastAPI
from typer import Typer

from .controller import Controller
from .middleware import MergeAppStateMiddleware
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
            command: Union[Callable, Typer] = import_attr(command)
            if isinstance(command, Typer):
                self.cli.add_typer(command)
            else:
                self.cli.command(command.__name__)(command)

    def include_controller(self, controller: Controller, **kwds):
        assert isinstance(
            controller, Controller
        ), f"Controller must be an instance of {controller!r}"
        router = controller.build(**kwds)
        self.include_router(router)


def create_app(settings: ModuleType, **kwds):
    kwds.setdefault("title", "Fastack")
    kwds.setdefault("description", "Fastack Framework")
    kwds.setdefault(
        "contact",
        {
            "name": "Fastack",
            "url": "https://github.com/aprilahijriyan/fastack",
        },
    )
    kwds["debug"] = settings.DEBUG
    app = Fastack(**kwds)
    app.add_middleware(MergeAppStateMiddleware)
    app.set_settings(settings)
    app.load_plugins()
    app.load_commands()
    return app
