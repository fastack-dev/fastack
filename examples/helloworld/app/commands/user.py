from typer import Typer, echo

from fastack.decorators import enable_context
from fastack.globals import current_app

cli = Typer(name="user", help="user command")


@cli.command()
@enable_context()
async def create():
    can_create_user = current_app.get_setting("CAN_CREATE_USER", False)
    if can_create_user:
        email = input("Email: ")
        echo(f"User email: {email}")
    else:
        echo("You can't create user")
