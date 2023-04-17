from fastapi import APIRouter, Depends

from domain.command.command_handler import CommandHandler
from infrastructure.notifier.client_notifier_factory import ClientNotifierFactory
from infrastructure.search.http_book_searcher import HttpBookSearcher
from infrastructure.subscriptions.mysql_subscription_repository import (
    MySQLSubscriptionsRepositoryFactory,
)
from use_cases.commands.sync_subscriptions_command import (
    SyncSubscriptionsCommand,
    SyncSubscriptionsCommandHandler,
)

sync_router = APIRouter()


async def _sync_subscriptions_command_handler() -> CommandHandler:
    subscriptions_repository = MySQLSubscriptionsRepositoryFactory.make()
    client_notifier = ClientNotifierFactory.make()
    book_searcher = HttpBookSearcher()
    return SyncSubscriptionsCommandHandler(
        subscriptions_repository, client_notifier, book_searcher
    )


@sync_router.get("/api/v1/subscriptions/sync")
def sync_subscriptions(
    sync_subscriptions_handler: SyncSubscriptionsCommandHandler = Depends(
        _sync_subscriptions_command_handler
    ),
) -> None:
    sync_subscriptions_handler.process(SyncSubscriptionsCommand())
