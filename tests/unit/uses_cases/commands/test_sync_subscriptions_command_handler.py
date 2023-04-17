from doublex import Mimic, Spy, Stub
from doublex_expects import have_been_called_with
from expects import expect

from domain.book import Book
from domain.client_notifier import ClientNotifier
from domain.subscriptions.subscription import Subscriptions
from infrastructure.notifier.console_client_notifier import ConsoleClientNotifier
from infrastructure.search.http_book_searcher import HttpBookSearcher
from infrastructure.subscriptions.json_subscriptions_repository import (
    JsonSubscriptionsRepository,
)
from use_cases.commands.sync_subscriptions_command import (
    SyncSubscriptionsCommand,
    SyncSubscriptionsCommandHandler,
)


class TestSyncSubscriptionsCommandHandler:
    def test_sync_subscriptions(self) -> None:
        books = [Book("any-title", "any-url", "any-image", 0)]
        subscriptions: Subscriptions = {"any-subscription": []}
        with Mimic(Stub, JsonSubscriptionsRepository) as repository:
            repository.find_all().returns(subscriptions)
        notifier: ClientNotifier = Mimic(Spy, ConsoleClientNotifier)
        with Mimic(Spy, HttpBookSearcher) as book_searcher:
            book_searcher.find_books("any-subscription").returns(books)

        handler = SyncSubscriptionsCommandHandler(repository, notifier, book_searcher)
        command = SyncSubscriptionsCommand()

        handler.process(command)

        expect(notifier.notify).to(have_been_called_with(subscriptions))
