from pydantic import BaseModel


class HelloWorldModel(BaseModel):
    id: int
    title: str
