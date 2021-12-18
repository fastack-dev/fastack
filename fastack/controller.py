from typing import Any, Sequence, Type, Union

from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from .constants import HTTP_METHODS, MAPPING_ENDPOINTS, METHOD_ENDPOINTS
from .pagination import PageNumberPagination, Pagination


class Controller:
    queryset: Any = None
    url_prefix: str = None
    mapping_endpoints = MAPPING_ENDPOINTS
    method_endpoints = METHOD_ENDPOINTS

    def get_url_prefix(self) -> str:
        c_name = "controller"
        prefix = self.url_prefix
        if not prefix:
            prefix = type(self).__name__.lower()
            if prefix.endswith(c_name):
                prefix = prefix.rstrip(c_name)
        return prefix

    def get_path(self, method: str) -> str:
        return self.mapping_endpoints.get(method) or ""

    def get_http_method(self, method: str) -> Union[str, None]:
        return self.method_endpoints.get(method) or None

    def build(self, **kwds) -> APIRouter:
        kwds.setdefault("prefix", self.get_url_prefix())
        router = APIRouter(**kwds)
        for method in dir(self):
            method = method.upper()
            if method not in HTTP_METHODS:
                method = self.get_http_method(method)

            if method:
                path = self.get_path(method)
                func = getattr(self, method)
                params = getattr(func, "__route_params__") or {}
                params.setdefault("methods", [method])
                router.add_api_route(path, func, **params)

        return router

    def json(
        self,
        detail: str,
        data: Union[dict, list] = None,
        status: int = 200,
        headers: dict = None,
    ) -> JSONResponse:
        content = {"detail": detail}
        if data:
            content["data"] = data
        return JSONResponse(content, status, headers=headers)


class RetrieveController(Controller):
    def retrieve(self, id: int) -> Response:
        raise NotImplementedError


class ListController(Controller):
    pagination_class: Type[Pagination] = PageNumberPagination

    def paginate(self, data: Sequence, page: int = 1, page_size: int = 10) -> Sequence:
        if self.pagination_class:
            return self.pagination_class(page, page_size).paginate(data)
        return data

    def get_paginated_response(
        self,
        data: Sequence,
        page: int = 1,
        page_size: int = 10,
        status: int = 200,
        headers: dict = None,
    ) -> JSONResponse:
        content = {
            "data": self.paginate(data, page, page_size),
            "page": page,
            "page_size": page_size,
            "total": len(data),
        }
        return JSONResponse(content, status_code=status, headers=headers)

    def list(self, page: int = 1, page_size: int = 10) -> Response:
        raise NotImplementedError


class CreateController(Controller):
    def create(self, body: BaseModel) -> Response:
        raise NotImplementedError


class UpdateController(Controller):
    def update(self, id: int) -> Response:
        raise NotImplementedError


class DestroyController(Controller):
    def destroy(self, id: int) -> Response:
        raise NotImplementedError


class ReadOnlyController(RetrieveController, ListController):
    pass


class CreateUpdateController(CreateController, UpdateController):
    pass
