from expects import be_empty, expect

from infrastructure.search.http_book_searcher import HttpBookSearcher


class TestHttpBookSearcher:
    def test_search_for_books(self) -> None:
        book_searcher = HttpBookSearcher()

        books = book_searcher.find_books("pendergast")

        expect(books).to_not(be_empty)
