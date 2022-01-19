from typing import Optional

from pydantic import AnyHttpUrl, BaseModel


class UserModel(BaseModel):
    id: int
    url: Optional[AnyHttpUrl]
