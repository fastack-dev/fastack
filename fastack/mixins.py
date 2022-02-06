from typing import Any, List, Optional, Sequence, Type

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .pagination import PageNumberPagination, Pagination


class ListControllerMixin:
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
            o = self.serialize_data(o)  # type: ignore[attr-defined]
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
