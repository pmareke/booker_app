from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from delivery.api.v1.create_one_subscription_router import create_one_router
from delivery.api.v1.delete_one_subscription_router import delete_one_router
from delivery.api.v1.find_all_subscriptions_router import find_all_router
from delivery.api.v1.find_one_subscription_router import find_one_router
from delivery.api.v1.sync_subscriptions_router import sync_router


app = FastAPI()

app.include_router(sync_router)
app.include_router(find_all_router)
app.include_router(find_one_router)
app.include_router(delete_one_router)
app.include_router(create_one_router)


def custom_openapi() -> dict:
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Booker",
        version="1.0.0",
        description="App to subscribe to a list of terms called subscriptions",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore
