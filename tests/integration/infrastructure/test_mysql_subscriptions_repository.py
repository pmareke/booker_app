import os

from expects import expect, have_keys, have_key, equal

from domain.book import Book
from domain.subscriptions.subscription import Subscriptions
from infrastructure.subscriptions.mysql_subscription_repository import (
    MySQLSubscriptionsRepositoryFactory,
)


class TestMySQLSubscriptionsRepository:
    def setup_method(self) -> None:
        os.environ["environment"] = "test"
        self.repository = MySQLSubscriptionsRepositoryFactory.make()

    def test_save_subscriptions(self) -> None:
        subscriptions_one = "test_save_subscriptions_one"
        subscriptions_two = "test_save_subscriptions_two"
        subscriptions: Subscriptions = {subscriptions_one: [], subscriptions_two: []}

        self.repository.save(subscriptions)

        repository_subscriptions = self.repository.find_all()
        expect(repository_subscriptions).to(
            have_keys(subscriptions_one, subscriptions_two)
        )

        self.repository.delete(subscriptions_one)
        self.repository.delete(subscriptions_two)

    def test_save_one_subscription(self) -> None:
        subscription = "test_save_one_subscription"
        self.repository.save_one(subscription)

        subscriptions = self.repository.find_all()

        expect(subscriptions).to(have_key(subscription))

        self.repository.delete("test_save_one_subscription")

    def test_find_all_subscriptions(self) -> None:
        subscription = "test_find_all_subscriptions"
        self.repository.save_one(subscription)

        subscriptions = self.repository.find_all()

        expect(subscriptions).to(have_key(subscription))

        self.repository.delete(subscription)

    def test_find_one_subscription(self) -> None:
        book = Book(title="any-title", url="any-url", image="any-image", timestamp=0)
        subscription_name = "test_find_one_subscription"
        subscription: Subscriptions = {subscription_name: [book]}
        self.repository.save(subscription)

        books = self.repository.find_books_by(subscription_name)

        expect(books[0].title).to(equal(book.title))
        expect(books[0].url).to(equal(book.url))
        expect(books[0].image).to(equal(book.image))
        expect(books[0].timestamp).to(equal(book.timestamp))

        self.repository.delete(subscription_name)

    def test_delete_one_subscription(self) -> None:
        subscription = "test"
        self.repository.save_one(subscription)

        self.repository.delete(subscription)

        subscriptions = self.repository.find_all()
        expect(subscriptions).not_to(have_key(subscription))
