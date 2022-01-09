from fastapi import Response
from pydantic import BaseModel

from fastack import ModelController
from fastack.decorators import route


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


class CustomController(UserController):
    name = "custom"
    url_prefix = "/custom"

    @route("/get/{id}", name="get_user")
    def retrieve(self, id: int) -> Response:
        return self.json("User", {"id": id, "url": self.url_for("get_user", id=id)})
