import json
from collections import defaultdict
from dataclasses import dataclass

from domain.book import Book, BookEncoder
from domain.subscriptions.subscription import Subscriptions
from domain.subscriptions.subscriptions_repository import SubscriptionsRepository

OLD_BOOKS_FILENAME = "books.json"


@dataclass
class BookResponse:
    title: str
    url: str
    image: str


class JsonSubscriptionsRepository(SubscriptionsRepository):
    def find_all(self) -> Subscriptions:
        subscriptions_file = self._read_subscription_file()
        subscriptions: Subscriptions = defaultdict(list)
        for subscription, books in subscriptions_file.items():
            subscriptions[subscription] = self._books_for_subscription(books)
        return subscriptions

    @staticmethod
    def _read_subscription_file() -> dict:
        with open(OLD_BOOKS_FILENAME) as file:
            return dict(json.load(file))

    @staticmethod
    def _books_for_subscription(books: list[dict]) -> list[Book]:
        return [
            Book(
                title=book["title"],
                timestamp=book["timestamp"],
                url=book["url"],
                image=book["image"],
            )
            for book in books
        ]

    def find_books_by(self, subscription: str) -> list[Book]:
        return self.find_all()[subscription]

    def delete(self, subscription: str) -> None:
        with open(OLD_BOOKS_FILENAME) as file:
            json_books = json.load(file)
            del json_books[subscription]
        with open(OLD_BOOKS_FILENAME, "w") as file:
            file.write(json.dumps(json_books))

    def save_one(self, subscription: str) -> None:
        with open(OLD_BOOKS_FILENAME) as file:
            json_books = json.load(file)
            json_books[subscription] = []
        with open(OLD_BOOKS_FILENAME, "w") as file:
            file.write(json.dumps(json_books))

    def save(self, subscriptions: Subscriptions) -> None:
        with open(OLD_BOOKS_FILENAME, "w") as file:
            json_subscriptions = json.dumps(subscriptions, indent=2, cls=BookEncoder)
            file.write(json_subscriptions)
