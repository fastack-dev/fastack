from enum import Enum

from mongoengine import fields

from fastack.plugins.mongoengine.base import Model


class Book(Model):
    class Status(str, Enum):
        DRAFT = "draft"
        PUBLISH = "publish"

    title = fields.StringField(max_length=255)
    status = fields.EnumField(Status, default=Status.DRAFT)
    published_date = fields.DateTimeField()

    def serialize(self) -> dict:
        data = super().serialize()
        data["title"] = self.title
        data["status"] = self.status
        data["published_date"] = self.published_date
        return data
