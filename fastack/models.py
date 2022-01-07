from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

GenericDataType = TypeVar("GenericDataType")


class DetailModel(GenericModel, Generic[GenericDataType]):
    """
    Schema to define data details in OpenAPI (for ``Controller.json`` method)
    """

    detail: Optional[str]
    data: Optional[GenericDataType]


class PagingModel(BaseModel):
    """
    Schema for part of ``paging`` field in ``PaginatedModel``.
    """

    next: Optional[int]
    prev: Optional[int]
    pages: List[int]


class PaginatedModel(GenericModel, Generic[GenericDataType]):
    """
    Schema for paged data (for ``ListController.get_paginated_response`` method)
    """

    total: Optional[int]
    paging: PagingModel
    data: List[GenericDataType]
