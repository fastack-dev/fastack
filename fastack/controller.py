from types import MethodType
from typing import Any, Callable, Dict, List, Optional, Sequence, Type, Union

from fastapi import APIRouter, params, routing
from fastapi.datastructures import Default
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRoute
from pydantic import BaseModel, conint
from starlette.routing import BaseRoute
from starlette.types import ASGIApp

from .constants import HTTP_METHODS, MAPPING_ENDPOINTS, METHOD_ENDPOINTS
from .pagination import PageNumberPagination, Pagination


class Controller:
    name: str = None
    url_prefix: str = None
    mapping_endpoints = MAPPING_ENDPOINTS
    method_endpoints = METHOD_ENDPOINTS

    def get_endpoint_name(self) -> str:
        if self.name:
            return self.name

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

    def build(
        self,
        *,
        prefix: str = "",
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
        default_response_class: Type[Response] = Default(JSONResponse),
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        routes: Optional[List[routing.BaseRoute]] = None,
        redirect_slashes: bool = True,
        default: Optional[ASGIApp] = None,
        dependency_overrides_provider: Optional[Any] = None,
        route_class: Type[APIRoute] = APIRoute,
        on_startup: Optional[Sequence[Callable[[], Any]]] = None,
        on_shutdown: Optional[Sequence[Callable[[], Any]]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
    ) -> APIRouter:
        endpoint_name = self.get_endpoint_name()
        tag_name = endpoint_name.replace("-", " ").title()
        if not tags:
            tags = [tag_name]

        if not prefix:
            prefix = self.get_url_prefix()

        router = APIRouter(
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
            default_response_class=default_response_class,
            responses=responses,
            callbacks=callbacks,
            routes=routes,
            redirect_slashes=redirect_slashes,
            default=default,
            dependency_overrides_provider=dependency_overrides_provider,
            route_class=route_class,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
        )
        for method_name in dir(self):
            func = getattr(self, method_name)
            if method_name.startswith("_") or not isinstance(func, MethodType):
                continue

            http_method = method_name.upper()
            if http_method not in HTTP_METHODS:
                http_method = self.get_http_method(method_name)

            is_action = getattr(func, "__route_action__", False)
            if http_method or is_action:
                name = f"{endpoint_name}:{method_name}"
                summary = f"{endpoint_name} {method_name.replace('_', ' ').title()}"
                default_path = self.get_path(method_name)
                params = getattr(func, "__route_params__", None) or {}
                if not params.get("methods", None):
                    params["methods"] = [http_method]

                if not params.get("name", None):
                    params["name"] = name

                if not params.get("summary", None):
                    params["summary"] = summary

                path = params.pop("path", None) or default_path
                router.add_api_route(path, func, **params)

        return router

    def serialize_data(self, obj: Any) -> Any:
        return obj.serialize()

    def json(
        self,
        detail: str,
        data: Union[dict, list, object] = None,
        *,
        status: int = 200,
        headers: dict = None,
        allow_empty: bool = True,
        **kwargs: Any,
    ) -> JSONResponse:
        content = {"detail": detail}
        if data or allow_empty:
            if hasattr(data, "serialize"):
                data = self.serialize_data(data)

            content["data"] = jsonable_encoder(data)

        return JSONResponse(content, status_code=status, headers=headers, **kwargs)


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
                o = self.serialize_data(o)

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
        *,
        status: int = 200,
        headers: dict = None,
        **kwargs: Any,
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
            "total": total,
            "paging": {"next": next_page, "prev": prev_page, "pages": pages},
            "data": self.paginate(data, page, page_size),
        }
        return JSONResponse(content, status_code=status, headers=headers, **kwargs)

    def list(self, page: conint(gt=0) = 1, page_size: conint(gt=0) = 10) -> Response:
        raise NotImplementedError


class CreateController(Controller):
    def create(self, body: BaseModel) -> Response:
        raise NotImplementedError


class UpdateController(Controller):
    def update(self, id: int, body: BaseModel) -> Response:
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
