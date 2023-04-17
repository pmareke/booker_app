import uuid

from domain.book import BookResponse
from domain.query.query import Query
from domain.query.query_handler import QueryHandler
from domain.query.query_response import QueryResponse
from domain.subscriptions.subscription import SubscriptionsResponse
from domain.subscriptions.subscriptions_repository import SubscriptionsRepository


class FindOneSubscriptionQuery(Query):
    def __init__(self, subscription: str) -> None:
        super().__init__(uuid.uuid1())
        self.subscription = subscription


class FindOneSubscriptionQueryResponse(QueryResponse):
    def __init__(self, subscription: SubscriptionsResponse) -> None:
        self.subscription = subscription


class FindOneSubscriptionQueryHandler(QueryHandler):
    def __init__(self, repository: SubscriptionsRepository):
        self.subscriptions_repository = repository

    def process(
        self, query: FindOneSubscriptionQuery
    ) -> FindOneSubscriptionQueryResponse:
        subscription = self.subscriptions_repository.find_books_by(query.subscription)
        books_response = [
            BookResponse(book.title, book.url, book.image) for book in subscription
        ]
        return FindOneSubscriptionQueryResponse({query.subscription: books_response})
