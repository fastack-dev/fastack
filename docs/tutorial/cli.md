# Command line interface

Fastack is very much inspired from flask which also provides command line like `flask` command called `fastack`.

Aims to make it easier for you to manage apps and also sometimes we need something, like add dummy data, run server, show app details, etc.

And I think this should be a *"mandatory feature"* for modern frameworks :D

## Create command

We use the `typer`, to create the command line. As we know, the creator of `typer` is also the creator of **FastAPI** too xD.

Let's make our first command:

```py title="app/commands/user.py"
from typer import Typer, echo

cli = Typer(name="user", help="user command")

@cli.command()
def create():
    """
    Create new user
    """
    email = input("Email: ")
    echo(f"User email: {email}")
```

Then add it to the app via the ``COMMANDS`` configuration:

```py
COMMANDS = [
    "app.commands.user.cli",
]
```

In the above example we will import the `cli` variable in `app/commands/user.py` and then put it into the `fastack` command.

Now we check the `user` command in `fastack`:

```
$ fastack user --help
Usage: fastack user [OPTIONS] COMMAND [ARGS]...

  user command

Options:
  --help  Show this message and exit.

Commands:
  create
```

If you run `fastack user create` it will ask you to enter `email` and print it in the console.

```
$ fastack user create
Email: hello@world.id
User email: hello@world.id
```

In the above example, we created a sub-command called `user` and now we are going to create only command instead of sub-command.

```py title="app/commands/user.py"
from typer import echo

def create():
    """
    Create new user
    """
    email = input("Email: ")
    echo(f"User email: {email}")
```

Then update the `COMMANDS` configuration to:

```py
COMMANDS = [
    "app.commands.user.create",
]
```

Let's see, if the `create` command is in the `fastack` command:

```
fastack --help
Usage: fastack [OPTIONS] COMMAND [ARGS]...

  fastack is an intuitive framework based on FastAPI.

Options:
  -v, --version                   Show version number and exit
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  create     Create new user
  new        Create project.
  routes     List all routes.
  runserver  Run app with uvicorn.

      fastack (c) 2021 - 2022 aprila hijriyan.
```

As you can see, the `create` command is available in `fastack` and is ready to use:

```
$ fastack create
Email: hello@mars.id
User email: hello@mars.id
```

For more information, you can visit the typer documentation directly at https://typer.tiangolo.com/


## Using application context on commands

To enable the application context, fastack provides a decorator called `enable_context` which allows you to fully access the app instance object without importing them. For example:

```py
from typer import echo
from fastack.decorators import enable_context
from fastack.globals import current_app

@enable_context()
def create():
    """
    Create new user
    """
    can_create_user = current_app.get_setting("CAN_CREATE_USER", False)
    if can_create_user:
        email = input("Email: ")
        echo(f"User email: {email}")
    else:
        echo("You can't create user")
```

what the `enable_context` decorator does here is:

1. Pushes the app instance object to the local context, which allows you to access it from `fastack.globals.current_app`.
2. Triggers `startup` and `shutdown` events in the application and allows you to access all plugins that are initialized at `startup` event via `fastack.globals.state`.


## Adding a global command using the entry point

We also support adding commands from global to the `fastack` CLI. This feature is also inspired by flask.

You can add global commands using the `fastack.commands` entry point group. First you have to create a python module or package, then configure the entry point as below:

=== "setup.py"

    ```py
    setup(
      ...,
      entry_points={
          'fastack.commands': [
              'awesome = awesome.cli:awesome_command',
          ],
      },
    )
    ```

=== "pyproject.toml (python-poetry)"

    ```toml
    [tool.poetry.plugins."fastack.commands"]
    awesome = "awesome.cli:awesome_command"
    ```

For more information about entry points, please visit the link below:

* https://stackoverflow.com/questions/774824/explain-python-entry-points
* https://setuptools.pypa.io/en/latest/pkg_resources.html#entry-points
