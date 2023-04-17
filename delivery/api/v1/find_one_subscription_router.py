from fastapi import APIRouter, Depends

from domain.query.query_handler import QueryHandler
from domain.subscriptions.subscription import SubscriptionsResponse
from infrastructure.subscriptions.mysql_subscription_repository import (
    MySQLSubscriptionsRepositoryFactory,
)
from use_cases.queries.find_one_subscription_query import (
    FindOneSubscriptionQuery,
    FindOneSubscriptionQueryHandler,
)

find_one_router = APIRouter()


async def _find_one_query_handler() -> QueryHandler:
    mysql_subscriptions_repository = MySQLSubscriptionsRepositoryFactory.make()
    return FindOneSubscriptionQueryHandler(mysql_subscriptions_repository)


@find_one_router.get("/api/v1/subscriptions/{subscription}")
def find_one_subscription(
    subscription: str,
    find_one_subscription_handler: FindOneSubscriptionQueryHandler = Depends(
        _find_one_query_handler
    ),
) -> SubscriptionsResponse:
    query = FindOneSubscriptionQuery(subscription)
    response = find_one_subscription_handler.process(query)
    return response.subscription
