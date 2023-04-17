from doublex import Mimic, Spy
from doublex_expects import have_been_called_with
from expects import expect

from domain.subscriptions.subscriptions_repository import SubscriptionsRepository
from infrastructure.subscriptions.json_subscriptions_repository import (
    JsonSubscriptionsRepository,
)
from use_cases.commands.create_one_subscription_command import (
    CreateOneSubscriptionCommandHandler,
    CreateOneSubscriptionCommand,
)


class TestCreateOneSubscriptionCommandHandler:
    def test_create_one_subscription(self) -> None:
        subscriptions_repository: SubscriptionsRepository = Mimic(
            Spy, JsonSubscriptionsRepository
        )
        handler = CreateOneSubscriptionCommandHandler(subscriptions_repository)
        command = CreateOneSubscriptionCommand("any-subscription")

        handler.process(command)

        expect(subscriptions_repository.save_one).to(
            have_been_called_with("any-subscription")
        )
