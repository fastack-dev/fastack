import os
from importlib import import_module
from types import ModuleType

APP_ENV: str = os.environ.get("APP_ENV", "local")

if "APP_SETTINGS_LOADED" not in os.environ:
    try:
        mod = import_module("app.settings." + APP_ENV)
    except ModuleNotFoundError:
        print(f"File configuration not found: {APP_ENV!r}")
        exit()
    else:
        for name in dir(mod):
            if not name.startswith("_"):
                value = getattr(mod, name)
                if not isinstance(value, ModuleType):
                    globals()[name] = value

        os.environ["APP_SETTINGS_LOADED"] = "1"
        del import_module, ModuleType, mod
