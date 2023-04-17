import os
from domain.client_notifier import ClientNotifier
from infrastructure.notifier.console_client_notifier import ConsoleClientNotifier
from infrastructure.notifier.email_client_notifier import EmailClientNotifier


class ClientNotifierFactory:
    @staticmethod
    def make() -> ClientNotifier:
        if os.getenv("environment"):
            return ConsoleClientNotifier()
        return EmailClientNotifier()
