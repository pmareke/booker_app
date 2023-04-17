from abc import ABC, abstractmethod

from domain.book import Book


class BookSearcher(ABC):
    @abstractmethod
    def find_books(self, search: str) -> list[Book]:
        raise NotImplementedError
