from types import MethodType
from typing import Any, Callable, Dict, List, Optional, Sequence, Type, Union

from fastapi import APIRouter, Query, params
from fastapi.datastructures import Default
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRoute
from pydantic import BaseModel
from starlette.routing import BaseRoute
from starlette.types import ASGIApp

from .constants import HTTP_METHODS, MAPPING_ENDPOINTS, METHOD_ENDPOINTS
from .pagination import PageNumberPagination, Pagination
from .utils import url_for


class Controller:
    """
    Base Controller for creating REST APIs.

    Example:

    ```python
    from pydantic import BaseModel

    class UserBody(BaseModel):
        name: str

    class UserController(Controller):
        def get(self, id: int):
            user = User.get(id)
            return self.json("User", user)

        def post(self, body: UserBody):
            user = User.create(**body.dict())
            return self.json("Created", user)

        def put(self, id: int, body: UserBody):
            user = User.get(id)
            user.update(**body.dict())
            return self.json("Updated", user)

        def delete(self, id: int):
            user = User.get(id)
            user.delete()
            return self.json("Deleted")

    user_controller = UserController()
    app.include_controller(user_controller)
    ```

    Attributes:
        name: Name of the controller. If not provided, the name of the class will be used.
        url_prefix: URL prefix of the controller. If not provided, the name of the controller will be used.
        mapping_endpoints: Mapping to get default path.
        method_endpoints: Mapping to get default HTTP method.
        middlewares: List of middlewares (dependencies) to be applied to all routes.

    """

    name: Optional[str] = None
    url_prefix: Optional[str] = None
    mapping_endpoints: Dict[str, str] = MAPPING_ENDPOINTS
    method_endpoints: Dict[str, str] = METHOD_ENDPOINTS
    middlewares: Optional[Sequence[params.Depends]] = []

    def get_endpoint_name(self) -> str:
        """
        Get the name of the controller.
        This will be used to prefix the endpoint name (e.g user)
        when you create the absolute path of an endpoint using ``request.url_for``
        it looks like this ``request.url_for('user:get')``

        ``get`` here is the method name (responder) so you cDict[str, str]an replace it according to the method name
        such as ``post``, ``put``, ``delete``, ``retrieve``, etc.

        Returns:
            str: Name of the controller.
        """
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

        # Save endpoint name
        self.name = rv.lower()
        return name

    def url_for(self, name: str, **params: Dict[str, Any]) -> str:
        """
        Generate absolute URL for an endpoint.

        Args:
            name: Method name (e.g. retrieve).
            params: Can be path parameters or query parameters.
        """

        endpoint_name = self.join_endpoint_name(name)
        return url_for(endpoint_name, **params)

    def get_url_prefix(self) -> str:
        """
        Get the URL prefix of the controller.
        If not provided, the name of the controller will be used.

        Returns:
            str: URL prefix of the controller.
        """

        prefix = self.url_prefix
        if not prefix:
            prefix = self.get_endpoint_name()
        prefix = "/" + prefix.lstrip("/")
        return prefix

    def get_path(self, method: str) -> str:
        """
        Get the path of an endpoint.

        Args:
            method: Name of the method.
        """

        return self.mapping_endpoints.get(method) or ""

    def get_http_method(self, method: str) -> Union[str, None]:
        """
        Get the HTTP method of an endpoint.

        Args:
            method: Name of the method.
        """
        return self.method_endpoints.get(method) or None

    def join_endpoint_name(self, name: str) -> str:
        """
        Join endpoint name with controller name.

        Args:
            name: Name of the method.
        """

        return self.get_endpoint_name() + ":" + name

    def build(
        self,
        *,
        prefix: str = "",
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
        default_response_class: Type[Response] = Default(JSONResponse),
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        routes: Optional[List[BaseRoute]] = None,
        redirect_slashes: bool = True,
        default: Optional[ASGIApp] = None,
        dependency_overrides_provider: Optional[Any] = None,
        route_class: Type[APIRoute] = APIRoute,
        on_startup: Optional[Sequence[Callable[[], Any]]] = None,
        on_shutdown: Optional[Sequence[Callable[[], Any]]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
    ) -> APIRouter:
        """
        Makes all APIs in controllers into a router (APIRouter)
        """

        endpoint_name = self.get_endpoint_name()
        tag_name = endpoint_name.replace("-", " ").title()
        if not tags:
            tags = [tag_name]

        if not prefix:
            prefix = self.get_url_prefix()

        if not dependencies:
            dependencies = []

        dependencies = dependencies + (self.middlewares or [])  # type: ignore[operator]
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
            # skip if it's not a method, valid methods shouldn't be prefixed with _
            if method_name.startswith("_") or not isinstance(func, MethodType):
                continue

            http_method: Optional[str] = method_name.upper()
            if http_method not in HTTP_METHODS:
                http_method = self.get_http_method(method_name)

            # Checks if a method has an HTTP method.
            # Also, if no HTTP method is found there is another option to add the method to the router.
            # Just need to mark method using ``fastack.decorators.route()`` decorator with ``action=True`` parameter.
            is_action = getattr(func, "__route_action__", False)
            if http_method or is_action:
                # To generate an absolute path, using request.url_for(...)
                summary = f"{endpoint_name} {method_name.replace('_', ' ').title()}"
                default_path = self.get_path(method_name)
                params = getattr(func, "__route_params__", None) or {}
                if not params.get("methods", None):
                    params["methods"] = [http_method]

                name = params.pop("name", None)
                if not name:
                    name = method_name

                params["name"] = self.join_endpoint_name(name)

                if not params.get("summary", None):
                    params["summary"] = summary

                # if no path is provided, use the default path
                path = params.pop("path", None) or default_path
                router.add_api_route(path, func, **params)

        return router

    def serialize_data(self, obj: Any) -> Any:
        """
        Serialize data to JSON.
        By default it will use the "serialize" method on the object to convert the data.
        """

        func = getattr(obj, "serialize", None)
        if callable(func):
            obj = func()
        return obj

    def json(
        self,
        detail: str,
        data: Optional[Union[dict, list, object]] = None,
        *,
        status: int = 200,
        headers: Optional[dict] = None,
        allow_empty: bool = True,
        **kwargs: Any,
    ) -> JSONResponse:
        """
        Return a JSON response.
        By default the json response will be formatted like this:

        ```json
        {
            "detail": "...",
            "data": ...
        }
        ```

        Args:
            detail: Detail of the response.
            data: Data to be serialized.
            status: HTTP status code.
            headers: HTTP headers.
            allow_empty: Allows blank data to be shown to frontend.
            **kwargs (optional): Additional arguments to be passed to the JSONResponse.
        """

        content = {"detail": detail}
        if data or allow_empty:
            data = self.serialize_data(data)
            content["data"] = jsonable_encoder(data)

        return JSONResponse(content, status_code=status, headers=headers, **kwargs)


class RetrieveController(Controller):
    """
    Controller for retrieving data.
    """

    def retrieve(self, id: int) -> Response:
        """
        Retrieve a single object with the given ID.
        """

        raise NotImplementedError  # pragma: no cover


class ListController(Controller):
    """
    Controller for listing data.

    Attributes:
        pagination_class: Class to be used for pagination.
    """

    pagination_class: Type[Pagination] = PageNumberPagination

    def paginate(self, data: Sequence, page: int = 1, page_size: int = 10) -> Sequence:
        """
        Paginate data.

        Args:
            data: Data to be paginated.
            page: Page number.
            page_size: Page size.

        """

        if self.pagination_class:
            data = self.pagination_class(page, page_size).paginate(data)

        results = []
        for o in data:
            o = self.serialize_data(o)
            o = jsonable_encoder(o)
            results.append(o)

        return results

    def get_total_data(self, data: Any):
        """
        Get total data.
        Might be useful if the data is a QuerySet or something that can compute :)
        """

        return len(data)

    def get_total_page(self, total: int, page_size: int = 10) -> List[int]:
        """
        Get total pages.

        Args:
            total: Total data.
            page_size: Page size.
        """

        if total == 0:
            return [1]  # pragma: no cover

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
        headers: Optional[dict] = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """
        Return a paginated response.

        Args:
            data: Data to be paginated.
            page: Page number.
            page_size: Page size.
            status: HTTP status code.
            headers: HTTP headers.
            **kwargs (optional): Additional arguments to be passed to the JSONResponse.
        """

        # Counting all pages
        total_data = self.get_total_data(data)
        pages = self.get_total_page(total_data, page_size)
        prev_page = page - 1
        if prev_page not in pages:
            prev_page = None  # type: ignore[assignment]

        next_page = page + 1
        if next_page not in pages:
            next_page = None  # type: ignore[assignment]

        # Get data per page
        data = self.paginate(data, page, page_size)
        total = self.get_total_data(data)
        content = {
            "total": total,
            "paging": {"next": next_page, "prev": prev_page, "pages": pages},
            "data": data,
        }
        return JSONResponse(content, status_code=status, headers=headers, **kwargs)

    def list(
        self, page: int = Query(1, gt=0), page_size: int = Query(10, gt=0)
    ) -> Response:
        """
        List data.
        """

        raise NotImplementedError  # pragma: no cover


class CreateController(Controller):
    """
    Controller for creating data.
    """

    def create(self, body: BaseModel) -> Response:
        """
        adding a new object.
        """

        raise NotImplementedError  # pragma: no cover


class UpdateController(Controller):
    """
    Controller for updating data.
    """

    def update(self, id: int, body: BaseModel) -> Response:
        """
        Update an object with the given ID.
        """

        raise NotImplementedError  # pragma: no cover


class DestroyController(Controller):
    """
    Controller for deleting data.
    """

    def destroy(self, id: int) -> Response:
        """
        Delete an object with the given ID.
        """

        raise NotImplementedError  # pragma: no cover


class ReadOnlyController(RetrieveController, ListController):
    """
    Controller for read-only data.
    """


class CreateUpdateController(CreateController, UpdateController):
    """
    Controller for creating and updating data.
    """


class ModelController(
    RetrieveController,
    CreateController,
    ListController,
    UpdateController,
    DestroyController,
):
    """
    Model Controller for creating REST APIs.
    """
