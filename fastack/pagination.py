from abc import ABCMeta, abstractmethod
from typing import Sequence


class Pagination(metaclass=ABCMeta):
    """
    Abstract class for pagination
    """

    def __init__(self, *args, **kwds) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def paginate(self, data: Sequence) -> Sequence:
        pass  # pragma: no cover


class PageNumberPagination(Pagination):
    """
    Pagination class for page number
    """

    def __init__(self, page: int, page_size: int):
        self.page = page
        self.page_size = page_size

    def get_offset(self) -> int:
        return self.page_size * (self.page - 1)

    def get_limit(self) -> int:
        return self.page_size

    def paginate(self, data: Sequence) -> Sequence:
        offset = self.get_offset()
        limit = self.get_limit()
        return data[offset : offset + limit]
