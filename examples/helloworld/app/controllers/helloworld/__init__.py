from fastapi import Response
from pydantic import conint

from fastack.controller import ReadOnlyController
from fastack.decorators import route
from fastack.models import DetailModel, PaginatedModel

from .models import HelloWorldModel


class HelloWorldController(ReadOnlyController):
    @route(response_model=PaginatedModel[HelloWorldModel])
    def list(self, page: conint(gt=0) = 1, page_size: conint(gt=0) = 10) -> Response:
        data = [{"id": i, "title": "Hello World"} for i in range(5)]
        return self.get_paginated_response(data, page, page_size)

    @route(response_model=DetailModel[HelloWorldModel])
    def retrieve(self, id: int) -> Response:
        return self.json("Detail", {"id": id, "title": "hello world"})

    @route(
        "/{id}/update",
        action=True,
        methods=["PUT"],
        response_model=DetailModel[HelloWorldModel],
    )
    def single_update(self, id: int) -> Response:
        return self.json("Update", {"id": id, "title": "hello mars"})
