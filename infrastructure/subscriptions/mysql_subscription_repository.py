import os
from collections import defaultdict

import MySQLdb

from domain.book import Book
from domain.subscriptions.subscription import Subscriptions
from domain.subscriptions.subscriptions_repository import SubscriptionsRepository


class MySQLSubscriptionsRepository(SubscriptionsRepository):
    def __init__(self, subscriptions_table: str, books_table: str) -> None:
        self.subscriptions_table = subscriptions_table
        self.books_table = books_table
        self.connection = MySQLdb.connect(
            host=os.getenv("DATASCALE_HOST"),
            user=os.getenv("DATASCALE_USERNAME"),
            passwd=os.getenv("DATASCALE_PASSWORD"),
            db=os.getenv("DATASCALE_DATABASE"),
            ssl_mode="VERIFY_IDENTITY",
            ssl={"ca": "/etc/ssl/certs/ca-certificates.crt"},
        )

    def find_all(self) -> Subscriptions:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * from {self.subscriptions_table}")
        database_subscriptions = cursor.fetchall()
        subscriptions: Subscriptions = defaultdict(list)
        for subscription in database_subscriptions:
            _, _, name = subscription
            books = self.find_books_by(name)
            subscriptions[name] = books
        return subscriptions

    def find_books_by(self, subscription: str) -> list[Book]:
        cursor = self.connection.cursor()
        subscription_id = self._find_id_by_subscription(subscription)
        cursor.execute(
            f"SELECT * from {self.books_table} WHERE subscription_id={subscription_id}"
        )
        books: list[Book] = []
        for book in cursor.fetchall():
            _, _, title, url, image, timestamp = book
            books.append(Book(title, url, image, timestamp))
        return books

    def delete(self, subscription: str) -> None:
        cursor = self.connection.cursor()
        subscription_id = self._find_id_by_subscription(subscription)
        cursor.execute(
            f"DELETE from {self.books_table} WHERE subscription_id={subscription_id}"
        )
        cursor.execute(
            f"DELETE from {self.subscriptions_table} WHERE name='{subscription}'"
        )
        self.connection.commit()

    def save_one(self, subscription: str) -> None:
        cursor = self.connection.cursor()
        subscription_id = self._find_id_by_subscription(subscription)
        if subscription_id:
            return
        cursor.execute(
            f"INSERT INTO {self.subscriptions_table} (name) VALUES ('{subscription}')"
        )
        self.connection.commit()

    def save(self, subscriptions: Subscriptions) -> None:
        for subscription, books in subscriptions.items():
            subscription_id = self._find_id_by_subscription(subscription)
            if not subscription_id:
                self.save_one(subscription)
            self._delete_old_books(subscription)
            self._save_book_for_subscription(subscription, books)
        self.connection.commit()

    def _find_id_by_subscription(self, subscription: str) -> int | None:
        cursor = self.connection.cursor()
        cursor.execute(
            f"SELECT id from {self.subscriptions_table} WHERE name='{subscription}'"
        )
        subscription_id = cursor.fetchone()
        return int(subscription_id[0]) if subscription_id else None

    def _delete_old_books(self, subscription: str) -> None:
        cursor = self.connection.cursor()
        subscription_id = self._find_id_by_subscription(subscription)
        cursor.execute(
            f"DELETE from {self.books_table} WHERE subscription_id='{subscription_id}'"
        )
        self.connection.commit()

    def _save_book_for_subscription(self, subscription: str, books: list[Book]) -> None:
        cursor = self.connection.cursor()
        subscription_id = self._find_id_by_subscription(subscription)
        for book in books:
            values = (subscription_id, book.title, book.url, book.image, book.timestamp)
            keys = "subscription_id, title, url, image, timestamp"
            cursor.execute(f"INSERT INTO {self.books_table} ({keys}) VALUES {values}")


class MySQLSubscriptionsRepositoryFactory:
    @staticmethod
    def make() -> MySQLSubscriptionsRepository:
        subscriptions_table = (
            "subscriptions_test" if os.getenv("environment") else "subscriptions"
        )
        books_table = "books_test" if os.getenv("environment") else "books"
        return MySQLSubscriptionsRepository(subscriptions_table, books_table)
