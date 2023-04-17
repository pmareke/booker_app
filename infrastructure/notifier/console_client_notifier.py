from domain.client_notifier import ClientNotifier
from domain.subscriptions.subscription import Subscriptions


class ConsoleClientNotifier(ClientNotifier):
    def notify(self, subscriptions: Subscriptions) -> None:
        for subscription, books in subscriptions.items():
            titles = [f"{book.title}" for book in books]
            separator = "-"[0] * max(len(title) for title in titles)
            print(
                "\n".join(
                    [separator, f"Query: {subscription}", "\n".join(titles), separator]
                )
            )
            print()
