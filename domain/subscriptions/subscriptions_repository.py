from abc import ABC, abstractmethod

from domain.book import Book
from domain.subscriptions.subscription import Subscriptions


class SubscriptionsRepository(ABC):
    @abstractmethod
    def find_all(self) -> Subscriptions:
        raise NotImplementedError

    @abstractmethod
    def find_books_by(self, subscription: str) -> list[Book]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, subscription: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def save_one(self, subscription: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def save(self, subscriptions: Subscriptions) -> None:
        raise NotImplementedError
