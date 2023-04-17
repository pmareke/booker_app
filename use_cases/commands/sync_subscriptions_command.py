import uuid
from collections import defaultdict

from domain.book_searcher import BookSearcher
from domain.client_notifier import ClientNotifier
from domain.command.command import Command
from domain.command.command_handler import CommandHandler
from domain.command.command_response import CommandResponse
from domain.subscriptions.subscription import Subscriptions
from domain.subscriptions.subscriptions_repository import SubscriptionsRepository


class SyncSubscriptionsCommand(Command):
    def __init__(self) -> None:
        super().__init__(uuid.uuid1())


class SyncSubscriptionsCommandResponse(CommandResponse):
    def __init__(self, subscriptions: Subscriptions) -> None:
        self.subscriptions = subscriptions


class SyncSubscriptionsCommandHandler(CommandHandler):
    def __init__(
        self,
        subscriptions_repository: SubscriptionsRepository,
        notifier: ClientNotifier,
        book_searcher: BookSearcher,
    ) -> None:
        self.subscriptions_repository = subscriptions_repository
        self.notifier = notifier
        self.book_searcher = book_searcher

    def process(
        self, _command: SyncSubscriptionsCommand
    ) -> SyncSubscriptionsCommandResponse:
        new_subscriptions = self._generate_new_subscriptions()
        self.notifier.notify(new_subscriptions)
        return SyncSubscriptionsCommandResponse(new_subscriptions)

    def _generate_new_subscriptions(self) -> Subscriptions:
        subscriptions = self.subscriptions_repository.find_all()
        new_subscriptions: Subscriptions = defaultdict(list)
        for subscription in subscriptions.keys():
            books = self.book_searcher.find_books(subscription)
            books_for_subscription = [
                book for book in books if book not in subscriptions[subscription]
            ]
            if books_for_subscription:
                new_subscriptions[subscription].extend(books_for_subscription)
                subscriptions[subscription] = new_subscriptions[subscription]
                self.subscriptions_repository.save(subscriptions)
        return new_subscriptions
