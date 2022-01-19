import os
import shutil

import pytest
from pkg_resources import get_distribution
from typer import Context, Typer, echo
from typer.testing import CliRunner

from fastack.app import Fastack
from fastack.decorators import command

os.environ["FASTACK_APP"] = "tests.app"

from fastack.__main__ import fastack

runner = CliRunner()


def execute(command: str):
    return runner.invoke(fastack, command)


def test_foo_command():
    with pytest.warns(DeprecationWarning, match="use enable_context instead"):
        result = execute("sub foo")
        assert result.stdout == "foo 321\n"


def test_bar_command():
    result = execute("bar")
    assert result.stdout == "initializer\nbar 123\nfinalizer\n"


def test_fastack_version():
    result = execute("--version")
    assert result.stdout == "fastack v%s\n" % get_distribution("fastack").version


def test_runserver():
    fastack.app = None
    result = execute("runserver")
    assert "Can't find app" in result.stdout


def test_merge_cli(app: Fastack):
    fastack.app = app
    with pytest.warns(DeprecationWarning, match="use enable_context instead"):
        result = execute("sub foo")
        assert result.stdout == "foo 321\n"

    sub_cmd = Typer(name="sub", help="sub_cmd help")

    @sub_cmd.command()
    def foo(ctx: Context):
        """foo"""
        echo("foo 123")

    three = Typer()
    three.add_typer(sub_cmd)
    fastack.merge(three)
    result = execute("sub foo")
    assert result.stdout == "foo 123\n"

    @command(name="runserver")
    def run():
        """runserver"""
        echo("tertipu kau bgst")

    fastack.merge(run)
    result = execute("runserver")
    assert result.stdout == "tertipu kau bgst\n"

    def runserver():
        """runserver"""
        echo("tertipu lagi kau bgst")

    fastack.merge(runserver)
    result = execute("runserver")
    assert result.stdout == "tertipu lagi kau bgst\n"


def test_new_command():
    project_name = "nama-proyek"
    execute("new " + project_name)
    assert os.path.isdir(project_name)
    shutil.rmtree(project_name)


def test_routes_command():
    result = execute("routes")
    assert "/api/test" in result.stdout
