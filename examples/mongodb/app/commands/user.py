from typer import Typer, echo

cli = Typer(name="user", help="user command")


@cli.command()
def create():
    email = input("Email: ")
    echo(f"User email: {email}")
