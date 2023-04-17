from abc import ABC, abstractmethod

from domain.subscriptions.subscription import Subscriptions


class ClientNotifier(ABC):
    @abstractmethod
    def notify(self, subscriptions: Subscriptions) -> None:
        raise NotImplementedError
