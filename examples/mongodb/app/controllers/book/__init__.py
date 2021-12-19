from typing import List

from app.models import Book
from fastapi import status
from pydantic import BaseModel, constr
from starlette.responses import Response

from fastack import CRUDController


class BodyBookModel(BaseModel):
    title: constr(max_length=255)
    status: Book.Status = Book.Status.DRAFT


class BookController(CRUDController):
    def retrieve(self, id: str) -> Response:
        book: Book = Book.objects(pk=id).first()
        if not book:
            return self.json("Not found", status=status.HTTP_404_NOT_FOUND)

        data: dict = book.serialize()
        return self.json("Detail book", data)

    def list(self, page: int = 1, page_size: int = 10) -> Response:
        books: List[Book] = Book.objects.all()
        return self.get_paginated_response(books, page, page_size)

    def create(self, body: BodyBookModel) -> Response:
        data = body.dict()
        book: Book = Book.create(**data)
        return self.json("Created", book)

    def update(self, id: str, body: BodyBookModel) -> Response:
        book: Book = Book.objects(pk=id).first()
        if not book:
            return self.json("Not found", status=status.HTTP_404_NOT_FOUND)

        data = body.dict()
        book.update(**data)
        return self.json("Updated", book)

    def destroy(self, id: str) -> Response:
        book: Book = Book.objects(pk=id).first()
        if not book:
            return self.json("Not found", status=status.HTTP_404_NOT_FOUND)

        book.delete()
        return self.json("Deleted")
