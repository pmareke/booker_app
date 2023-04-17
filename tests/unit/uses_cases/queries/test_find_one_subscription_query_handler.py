from doublex import Mimic, Stub
from expects import equal, expect

from domain.book import Book, BookResponse
from domain.subscriptions.subscription import SubscriptionsResponse
from infrastructure.subscriptions.json_subscriptions_repository import (
    JsonSubscriptionsRepository,
)
from use_cases.queries.find_one_subscription_query import (
    FindOneSubscriptionQuery,
    FindOneSubscriptionQueryHandler,
)


class TestFindOneSubscriptionsQueryHandler:
    def test_find_one_subscription(self) -> None:
        books = [Book("any-title", "any-url", "any-image", 0)]
        subscriptions_response: SubscriptionsResponse = {
            "any-subscription": [BookResponse("any-title", "any-url", "any-image")]
        }
        with Mimic(Stub, JsonSubscriptionsRepository) as subscriptions_repository:
            subscriptions_repository.find_books_by("any-subscription").returns(books)

        handler = FindOneSubscriptionQueryHandler(subscriptions_repository)
        query = FindOneSubscriptionQuery("any-subscription")

        response = handler.process(query)

        expect(response.subscription).to(equal(subscriptions_response))
