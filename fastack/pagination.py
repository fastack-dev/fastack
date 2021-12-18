from abc import ABCMeta, abstractmethod
from typing import Sequence


class Pagination(metaclass=ABCMeta):
    @abstractmethod
    def paginate(self, data: Sequence) -> Sequence:
        pass


class PageNumberPagination(Pagination):
    def __init__(self, page: int, page_size: int):
        self.page = page
        self.page_size = page_size

    def get_offset(self):
        return self.page_size * (self.page - 1)

    def get_limit(self):
        return self.page_size

    def paginate(self, data: Sequence):
        offset = self.get_offset()
        limit = self.get_limit()
        return data[offset : offset + limit]
