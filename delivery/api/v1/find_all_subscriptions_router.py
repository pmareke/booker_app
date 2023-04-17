from fastapi import APIRouter, Depends

from domain.query.query_handler import QueryHandler
from domain.subscriptions.subscription import SubscriptionsResponse
from infrastructure.subscriptions.mysql_subscription_repository import (
    MySQLSubscriptionsRepositoryFactory,
)
from use_cases.queries.find_all_subscriptions_query import (
    FindAllSubscriptionsQueryHandler,
    FindAllSubscriptionsQuery,
)

find_all_router = APIRouter()


async def _find_all_query_handler() -> QueryHandler:
    mysql_subscriptions_repository = MySQLSubscriptionsRepositoryFactory.make()
    return FindAllSubscriptionsQueryHandler(mysql_subscriptions_repository)


@find_all_router.get("/api/v1/subscriptions")
def find_all_subscriptions(
    find_all_subscriptions_handler: FindAllSubscriptionsQueryHandler = Depends(
        _find_all_query_handler
    ),
) -> SubscriptionsResponse:
    response = find_all_subscriptions_handler.process(FindAllSubscriptionsQuery())
    return response.subscriptions
