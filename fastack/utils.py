from importlib import import_module


def import_attr(module: str):
    package, attr = module.rsplit(".", 1)
    module = import_module(package)
    return getattr(module, attr)
