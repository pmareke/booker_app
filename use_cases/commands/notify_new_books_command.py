import uuid

from domain.client_notifier import ClientNotifier
from domain.command.command import Command
from domain.command.command_handler import CommandHandler
from domain.command.command_response import CommandResponse
from domain.subscriptions.subscription import Subscriptions


class NotifyNewBooksCommand(Command):
    def __init__(self, subscriptions: Subscriptions) -> None:
        super().__init__(uuid.uuid1())
        self.subscriptions = subscriptions


class NotifyNewBooksCommandResponse(CommandResponse):
    pass


class NotifyNewBooksCommandHandler(CommandHandler):
    def __init__(self, client_notifier: ClientNotifier) -> None:
        self.client_notifier = client_notifier

    def process(self, command: NotifyNewBooksCommand) -> NotifyNewBooksCommandResponse:
        self.client_notifier.notify(command.subscriptions)
        return NotifyNewBooksCommandResponse()
