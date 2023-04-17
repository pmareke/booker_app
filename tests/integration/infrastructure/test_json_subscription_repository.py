from expects import expect, have_len

from infrastructure.subscriptions.json_subscriptions_repository import (
    JsonSubscriptionsRepository,
)


class TestJsonSubscriptionRepopsitory:
    def test_create_and_delete_one_subscription(self) -> None:
        subscription = "any-subscription"
        json_subscriptions_repository = JsonSubscriptionsRepository()

        json_subscriptions_repository.save_one(subscription)
        subscriptions = json_subscriptions_repository.find_all()

        expect(subscriptions).to(have_len(1))

        json_subscriptions_repository.delete(subscription)
        subscriptions = json_subscriptions_repository.find_all()
        expect(subscriptions).to(have_len(0))
