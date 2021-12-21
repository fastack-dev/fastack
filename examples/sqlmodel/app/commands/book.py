from typing import List

from app.models import Book
from sqlalchemy.sql.expression import asc
from sqlmodel import Session
from typer import Context, Typer, echo

from fastack import Fastack
from fastack.decorators import with_asgi_lifespan

cli = Typer(name="book", help="Book manager")


def open_db(app: Fastack) -> Session:
    session: Session = app.state.db.open()
    return session


@cli.command()
@with_asgi_lifespan
def add(ctx: Context):
    """Add a new book"""

    title = input("title: ")
    status = Book.Status(input("status (draft or publish): "))
    session = open_db(ctx.obj)
    with session:
        Book.create(session, title=title, status=status)

    print("Book added")


@cli.command()
@with_asgi_lifespan
def list(ctx: Context):
    """List all books"""

    session = open_db(ctx.obj)
    with session:
        books = session.query(Book).order_by(asc(Book.id)).all()
        for book in books:
            echo(f"{book.id}. {book.title} ({book.status})")


@cli.command()
@with_asgi_lifespan
def delete(ctx: Context):
    """Delete a book"""

    id = input("id: ")
    session = open_db(ctx.obj)
    with session:
        book: Book = session.query(Book).filter(Book.id == id).first()
        if book is None:
            echo("Book not found")
            return

        book.delete(session)
        echo(f"Book deleted")


@cli.command()
@with_asgi_lifespan
def update(ctx: Context):
    """Update a book"""

    id = input("id: ")
    title = input("title: ")
    status = Book.Status(input("status (draft or publish): "))
    session = open_db(ctx.obj)
    with session.begin():
        book: Book = session.query(Book).filter(Book.id == id).first()
        if book is None:
            echo("Book not found")
            return

        book.title = title
        book.status = status
        book.save(session)
        echo("Book updated")


@cli.command()
@with_asgi_lifespan
def search(ctx: Context):
    """Search for books"""

    title = input("title: ")
    session = open_db(ctx.obj)
    with session:
        books: List[Book] = (
            session.query(Book)
            .filter(Book.title.contains(title))
            .distinct(Book.title)
            .all()
        )
        for book in books:
            echo(f"{book.id}. {book.title}")
