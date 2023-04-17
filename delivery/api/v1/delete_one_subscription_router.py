from fastapi import APIRouter, Depends
from starlette import status

from domain.command.command_handler import CommandHandler
from infrastructure.subscriptions.mysql_subscription_repository import (
    MySQLSubscriptionsRepositoryFactory,
)
from use_cases.commands.delete_one_subscription_command import (
    DeleteOneSubscriptionCommandHandler,
    DeleteOneSubscriptionCommand,
)

delete_one_router = APIRouter()


async def _delete_one_subscription_command_handler() -> CommandHandler:
    mysql_subscriptions_repository = MySQLSubscriptionsRepositoryFactory.make()
    return DeleteOneSubscriptionCommandHandler(mysql_subscriptions_repository)


@delete_one_router.delete(
    "/api/v1/subscriptions/{subscription}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_one_subscription(
    subscription: str,
    delete_one_subscription_handler: DeleteOneSubscriptionCommandHandler = Depends(
        _delete_one_subscription_command_handler
    ),
) -> None:
    delete_one_subscription_handler.process(DeleteOneSubscriptionCommand(subscription))
