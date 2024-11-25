import asyncio

from fastapi import FastAPI

from src.api.lifespan import start_broker, stop_broker, run_migrations
from src.api.routers.insurance_handlers import router as insurance_router
from src.api.routers.tariff_handlers import router as tariff_router


def get_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router=tariff_router)
    app.include_router(router=insurance_router)

    @app.on_event("startup")
    async def on_start():
        await run_migrations()
        while True:
            try:
                await start_broker()
                print("Kafka is ready!")
                break
            except Exception as e:
                print(f"Waiting for Kafka... {e}")
                await asyncio.sleep(5)

    @app.on_event("shutdown")
    async def on_close():
        await stop_broker()

    return app
