import os

from expects import expect, be
from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestBooker:
    @staticmethod
    def setup_method() -> None:
        os.environ["environment"] = "test"

    def test_search_subscriptions(self) -> None:
        subscription = "test_search_subscriptions"

        response = client.post(f"/api/v1/subscriptions?subscription={subscription}")
        expect(response.status_code).to(be(status.HTTP_201_CREATED))

        response = client.get("/api/v1/subscriptions")
        expect(response.status_code).to(be(status.HTTP_200_OK))

        response = client.get(f"/api/v1/subscriptions/{subscription}")
        expect(response.status_code).to(be(status.HTTP_200_OK))

        client.delete(f"/api/v1/subscriptions/{subscription}")

    def test_sync_subscriptions(self) -> None:
        subscription = "test_sync_subscriptions"

        response = client.post(f"/api/v1/subscriptions?subscription={subscription}")
        expect(response.status_code).to(be(status.HTTP_201_CREATED))

        response = client.get("/api/v1/subscriptions/sync")
        expect(response.status_code).to(be(status.HTTP_200_OK))

        client.delete(f"/api/v1/subscriptions/{subscription}")
