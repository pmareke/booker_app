import requests

from domain.book import Book, BooksFactory
from domain.book_searcher import BookSearcher


class HttpBookSearcher(BookSearcher):
    def find_books(self, search: str) -> list[Book]:
        raise NotImplementedError
