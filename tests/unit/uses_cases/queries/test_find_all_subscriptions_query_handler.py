from doublex import Mimic, Stub
from expects import equal, expect

from domain.book import Book, BookResponse
from domain.subscriptions.subscription import Subscriptions, SubscriptionsResponse
from infrastructure.subscriptions.json_subscriptions_repository import (
    JsonSubscriptionsRepository,
)
from use_cases.queries.find_all_subscriptions_query import (
    FindAllSubscriptionsQuery,
    FindAllSubscriptionsQueryHandler,
)


class TestFindAllSubscriptionsQueryHandler:
    def test_find_all_subscriptions(self) -> None:
        subscriptions: Subscriptions = {
            "any-subscription": [Book("any-title", "any-url", "any-image", 0)]
        }
        subscriptions_response: SubscriptionsResponse = {
            "any-subscription": [BookResponse("any-title", "any-url", "any-image")]
        }
        with Mimic(Stub, JsonSubscriptionsRepository) as subscriptions_repository:
            subscriptions_repository.find_all().returns(subscriptions)

        handler = FindAllSubscriptionsQueryHandler(subscriptions_repository)
        query = FindAllSubscriptionsQuery()

        response = handler.process(query)

        expect(response.subscriptions).to(equal(subscriptions_response))
