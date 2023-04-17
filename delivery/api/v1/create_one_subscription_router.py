from fastapi import APIRouter, Depends
from starlette import status

from domain.command.command_handler import CommandHandler
from infrastructure.notifier.client_notifier_factory import ClientNotifierFactory
from infrastructure.search.http_book_searcher import HttpBookSearcher
from infrastructure.subscriptions.mysql_subscription_repository import (
    MySQLSubscriptionsRepositoryFactory,
)
from use_cases.commands.create_one_subscription_command import (
    CreateOneSubscriptionCommandHandler,
    CreateOneSubscriptionCommand,
)
from use_cases.commands.sync_subscriptions_command import (
    SyncSubscriptionsCommand,
    SyncSubscriptionsCommandHandler,
)

create_one_router = APIRouter()


async def _create_one_subscription_command_handler() -> CommandHandler:
    mysql_subscriptions_repository = MySQLSubscriptionsRepositoryFactory.make()
    return CreateOneSubscriptionCommandHandler(mysql_subscriptions_repository)


async def _sync_subscriptions_command_handler() -> CommandHandler:
    mysql_subscriptions_repository = MySQLSubscriptionsRepositoryFactory.make()
    client_notifier = ClientNotifierFactory.make()
    book_searcher = HttpBookSearcher()
    return SyncSubscriptionsCommandHandler(
        mysql_subscriptions_repository, client_notifier, book_searcher
    )


@create_one_router.post("/api/v1/subscriptions", status_code=status.HTTP_201_CREATED)
def create_one_subscription(
    subscription: str,
    create_one_subscription_handler: CreateOneSubscriptionCommandHandler = Depends(
        _create_one_subscription_command_handler
    ),
    sync_subscriptions_handler: SyncSubscriptionsCommandHandler = Depends(
        _sync_subscriptions_command_handler
    ),
) -> None:
    create_one_subscription_handler.process(CreateOneSubscriptionCommand(subscription))
    sync_subscriptions_handler.process(SyncSubscriptionsCommand())
