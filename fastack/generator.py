from distutils.dir_util import copy_tree
from pathlib import Path

from typer import colors, echo

TEMPLATE_PATH = Path(__file__).resolve().parent / "templates"


def create_project(name: str):
    dst = Path.cwd() / name
    if dst.exists():
        echo(f"Project {name} already exist", color=colors.BRIGHT_YELLOW)
        exit(1)

    dst.mkdir(exist_ok=True)
    src = str(TEMPLATE_PATH)
    copy_tree(src, str(dst))
