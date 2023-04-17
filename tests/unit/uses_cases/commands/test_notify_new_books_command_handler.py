from doublex import Mimic, Spy
from doublex_expects import have_been_called_with
from expects import expect

from domain.book import Book
from domain.client_notifier import ClientNotifier
from domain.subscriptions.subscription import Subscriptions
from infrastructure.notifier.console_client_notifier import ConsoleClientNotifier
from use_cases.commands.notify_new_books_command import (
    NotifyNewBooksCommand,
    NotifyNewBooksCommandHandler,
)


class TestNotifyNewBooksCommandHandler:
    def test_notifies_about_new_books(self) -> None:
        subscriptions: Subscriptions = {
            "any-subscription": [Book("any-title", "any-url", "any-image", 0)]
        }
        notifier: ClientNotifier = Mimic(Spy, ConsoleClientNotifier)

        handler = NotifyNewBooksCommandHandler(notifier)
        command = NotifyNewBooksCommand(subscriptions)

        handler.process(command)

        expect(notifier.notify).to(have_been_called_with(subscriptions))
