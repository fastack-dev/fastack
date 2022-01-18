from fastapi import Query, Response
from pydantic import BaseModel

from fastack import Controller, ModelController
from fastack.decorators import route

from .plugin import say_hello


class UserBody(BaseModel):
    name: str


class UserController(ModelController):
    def retrieve(self, id: int) -> Response:
        return self.json("User", {"id": id, "url": self.url_for("retrieve", id=id)})

    def create(self, body: UserBody) -> Response:
        return self.json("Created", body.dict())

    def update(self, id: int, body: UserBody) -> Response:
        return self.json("Updated", {"id": id, **body.dict()})

    def destroy(self, id: int) -> Response:
        return self.json("Deleted", {"id": id})

    @route(name="list")
    def list(
        self, page: int = Query(1, gt=0), page_size: int = Query(10, gt=0)
    ) -> Response:
        data = [{"number": x, "url": self.url_for("list")} for x in range(1, 21)]
        return self.get_paginated_response(data, page, page_size)


class CustomController(UserController):
    name = "custom"
    url_prefix = "/custom"

    @route("/get/{id}", name="get_user")
    async def retrieve(self, id: int) -> Response:
        return self.json("User", {"id": id, "url": self.url_for("get_user", id=id)})


class PluginYoiController(Controller):
    def get(self):
        word = "Hello "
        if say_hello:
            word += "there!"
        else:
            word += "world!"

        class Obj:
            msg = word

            def serialize(self):
                return {"msg": self.msg}

        return self.json("Yoi", Obj())
