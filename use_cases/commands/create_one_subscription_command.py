import uuid

from domain.command.command import Command
from domain.command.command_handler import CommandHandler
from domain.command.command_response import CommandResponse
from domain.subscriptions.subscriptions_repository import SubscriptionsRepository


class CreateOneSubscriptionCommand(Command):
    def __init__(self, subscription: str) -> None:
        super().__init__(uuid.uuid1())
        self.subscription = subscription


class CreateOneSubscriptionCommandResponse(CommandResponse):
    pass


class CreateOneSubscriptionCommandHandler(CommandHandler):
    def __init__(self, subscriptions_repository: SubscriptionsRepository) -> None:
        self.subscriptions_repository = subscriptions_repository

    def process(
        self, command: CreateOneSubscriptionCommand
    ) -> CreateOneSubscriptionCommandResponse:
        self.subscriptions_repository.save_one(command.subscription)
        return CreateOneSubscriptionCommandResponse()
