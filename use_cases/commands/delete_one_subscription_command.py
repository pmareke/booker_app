import uuid

from domain.command.command import Command
from domain.command.command_handler import CommandHandler
from domain.command.command_response import CommandResponse
from domain.subscriptions.subscriptions_repository import SubscriptionsRepository


class DeleteOneSubscriptionCommand(Command):
    def __init__(self, subscription: str) -> None:
        super().__init__(uuid.uuid1())
        self.subscription = subscription


class DeleteOneSubscriptionCommandResponse(CommandResponse):
    pass


class DeleteOneSubscriptionCommandHandler(CommandHandler):
    def __init__(self, subscriptions_repository: SubscriptionsRepository) -> None:
        self.subscriptions_repository = subscriptions_repository

    def process(
        self, command: DeleteOneSubscriptionCommand
    ) -> DeleteOneSubscriptionCommandResponse:
        self.subscriptions_repository.delete(command.subscription)
        return DeleteOneSubscriptionCommandResponse()
