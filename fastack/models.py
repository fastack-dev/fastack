from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

GenericDataType = TypeVar("GenericDataType")


class DetailModel(GenericModel, Generic[GenericDataType]):
    detail: Optional[str]
    data: Optional[GenericDataType]


class PagingModel(BaseModel):
    next: Optional[int]
    prev: Optional[int]
    pages: List[int]


class PaginatedModel(GenericModel, Generic[GenericDataType]):
    total: Optional[int]
    paging: PagingModel
    data: List[GenericDataType]
