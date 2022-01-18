import os

import pytest
from pkg_resources import get_distribution
from typer import Context, Typer, echo
from typer.testing import CliRunner

from fastack.decorators import command

env = os.environ
env["FASTACK_APP"] = "tests.app"
runner = CliRunner(env=env)
from fastack.__main__ import fastack as app


def execute(command: str):
    return runner.invoke(app, command)


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


def test_merge_cli():
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
    app.merge(three)
    result = execute("sub foo")
    assert result.stdout == "foo 123\n"

    @command(name="runserver")
    def run():
        """runserver"""
        echo("tertipu kau bgst")

    app.merge(run)
    result = execute("runserver")
    assert result.stdout == "tertipu kau bgst\n"

    def runserver():
        """runserver"""
        echo("tertipu lagi kau bgst")

    app.merge(runserver)
    result = execute("runserver")
    assert result.stdout == "tertipu lagi kau bgst\n"
