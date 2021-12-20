from types import MethodType
from typing import Any, List, Sequence, Type, Union

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, conint

from .constants import HTTP_METHODS, MAPPING_ENDPOINTS, METHOD_ENDPOINTS
from .pagination import PageNumberPagination, Pagination


class Controller:
    queryset: Any = None
    url_prefix: str = None
    mapping_endpoints = MAPPING_ENDPOINTS
    method_endpoints = METHOD_ENDPOINTS

    def get_endpoint_name(self) -> str:
        c_suffix = "controller"
        name = type(self).__name__
        # remove "controller" text if any
        if len(name) > len(c_suffix):
            sfx = name[len(name) - len(c_suffix) :].lower()
            if sfx == c_suffix:
                name = name[: len(name) - len(c_suffix)]

        rv = ""
        for c in name:
            if c.isupper() and len(rv) > 0:
                c = "-" + c
            rv += c

        return rv.lower()

    def get_url_prefix(self) -> str:
        prefix = self.url_prefix
        if not prefix:
            prefix = self.get_endpoint_name()
        prefix = "/" + prefix.lstrip("/")
        return prefix

    def get_path(self, method: str) -> str:
        return self.mapping_endpoints.get(method) or ""

    def get_http_method(self, method: str) -> Union[str, None]:
        return self.method_endpoints.get(method) or None

    def build(self, **kwds) -> APIRouter:
        endpoint_name = self.get_endpoint_name().replace("-", " ").title()
        kwds.setdefault("tags", [endpoint_name])
        kwds.setdefault("prefix", self.get_url_prefix())
        router = APIRouter(**kwds)
        for method_name in dir(self):
            func = getattr(self, method_name)
            if method_name.startswith("_") or not isinstance(func, MethodType):
                continue

            http_method = method_name.upper()
            if http_method not in HTTP_METHODS:
                http_method = self.get_http_method(method_name)

            if http_method:
                summary = f"{endpoint_name} {method_name.title()}"
                path = self.get_path(method_name)
                params = getattr(func, "__route_params__", None) or {}
                params.setdefault("methods", [http_method])
                params.setdefault("name", method_name)
                params.setdefault("summary", summary)
                router.add_api_route(path, func, **params)

        return router

    def json(
        self,
        detail: str,
        data: Union[dict, list, object] = None,
        status: int = 200,
        headers: dict = None,
    ) -> JSONResponse:
        content = {"detail": detail}
        if data:
            if hasattr(data, "serialize"):
                data = data.serialize()

            content["data"] = jsonable_encoder(data)

        return JSONResponse(content, status, headers=headers)


class RetrieveController(Controller):
    def retrieve(self, id: int) -> Response:
        raise NotImplementedError


class ListController(Controller):
    pagination_class: Type[Pagination] = PageNumberPagination

    def paginate(self, data: Sequence, page: int = 1, page_size: int = 10) -> Sequence:
        if self.pagination_class:
            data = self.pagination_class(page, page_size).paginate(data)

        results = []
        for o in data:
            if hasattr(o, "serialize"):
                o = o.serialize()

            o = jsonable_encoder(o)
            results.append(o)

        return results

    def get_total_data(self, data: Any):
        return len(data)

    def get_total_page(self, total: int, page_size: int = 10) -> List[int]:
        if total == 0:
            return [1]

        return list(
            range(
                1,
                (
                    total // page_size + 1
                    if total % page_size != 0
                    else total // page_size
                )
                + 1,
            )
        )

    def get_paginated_response(
        self,
        data: Sequence,
        page: int = 1,
        page_size: int = 10,
        status: int = 200,
        headers: dict = None,
    ) -> JSONResponse:
        total = self.get_total_data(data)
        pages = self.get_total_page(total, page_size)
        prev_page = page - 1
        if prev_page < 1:
            prev_page = None

        next_page = page + 1
        if next_page not in pages:
            next_page = None

        content = {
            "data": self.paginate(data, page, page_size),
            "paging": {"prev": prev_page, "next": next_page, "pages": pages},
            "total": total,
        }
        return JSONResponse(content, status_code=status, headers=headers)

    def list(self, page: conint(gt=0) = 1, page_size: conint(gt=0) = 10) -> Response:
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


class CRUDController(
    RetrieveController,
    CreateController,
    ListController,
    UpdateController,
    DestroyController,
):
    pass
