from dataclasses import dataclass
from json import JSONEncoder


@dataclass
class Book:
    title: str
    url: str
    image: str
    timestamp: int

    def __eq__(self, other_book: object) -> bool:
        return self.timestamp != other_book.timestamp  # type: ignore

    def __hash__(self) -> int:
        return hash(self.title)


@dataclass
class BookResponse:
    title: str
    url: str
    image: str


class BookEncoder(JSONEncoder):
    def default(self, o: Book) -> dict:
        return o.__dict__


class BooksFactory:
    @staticmethod
    def from_dict(response: dict) -> list[Book]:
        books: list[Book] = []
        for doc in response["content"]["docs"]:
            if doc["productType"] == "Libro":
                book = Book(
                    title=doc["name"],
                    url=doc["url"],
                    image=doc["image"],
                    timestamp=int(doc["dateRelease"]),
                )
                books.append(book)
        sorted_books: list[Book] = sorted(
            set(books), key=lambda b: b.timestamp, reverse=True
        )
        return sorted_books
