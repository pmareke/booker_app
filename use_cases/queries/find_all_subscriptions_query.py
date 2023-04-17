import uuid
from collections import defaultdict

from domain.book import BookResponse
from domain.query.query import Query
from domain.query.query_handler import QueryHandler
from domain.query.query_response import QueryResponse
from domain.subscriptions.subscription import Subscriptions, SubscriptionsResponse
from domain.subscriptions.subscriptions_repository import SubscriptionsRepository


class FindAllSubscriptionsQuery(Query):
    def __init__(self) -> None:
        super().__init__(uuid.uuid1())


class FindAllSubscriptionsQueryResponse(QueryResponse):
    def __init__(self, subscriptions: SubscriptionsResponse) -> None:
        self.subscriptions = subscriptions


class FindAllSubscriptionsQueryHandler(QueryHandler):
    def __init__(self, repository: SubscriptionsRepository):
        self.subscriptions_repository = repository

    def process(
        self, _query: FindAllSubscriptionsQuery
    ) -> FindAllSubscriptionsQueryResponse:
        subscriptions: Subscriptions = self.subscriptions_repository.find_all()
        return FindAllSubscriptionsQueryResponse(
            self._transform_to_book_response(subscriptions)
        )

    @staticmethod
    def _transform_to_book_response(
        subscriptions: Subscriptions,
    ) -> SubscriptionsResponse:
        subscriptions_response: SubscriptionsResponse = defaultdict(list)
        for subscription, books in subscriptions.items():
            subscription_books = [
                BookResponse(book.title, book.url, book.image) for book in books
            ]
            subscriptions_response[subscription] = subscription_books
        return subscriptions_response
