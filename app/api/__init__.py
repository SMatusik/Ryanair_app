import asyncio
import logging

from fastapi import FastAPI
from messente_api import (
    Configuration as MessenteConfiguration,
    OmnimessageApi,
    ApiClient,
)

from app.utils.password_hash import PasswordHash, password_hash
from ryanair import Ryanair
from app.api.ryanair import router as ryanair_router
from app.api.airports import router as airports_router
from app.api.users import router as users_router
from app.config import read_config
from app.constants import CURRENCY
from app.services import ServiceLayer
from app.services.messente import MessenteService
from app.services.ryanair import RyanAirService
from app.tasks.ryanair_tasks import check_price
import airportsdata

logger = logging.getLogger(__name__)


def create_api() -> FastAPI:
    app = FastAPI()
    config = read_config()
    app.include_router(ryanair_router)
    app.include_router(airports_router)
    app.include_router(users_router)

    @app.on_event("startup")
    async def startup() -> None:
        ryanair_service = RyanAirService(api=Ryanair(CURRENCY), threshold=1)
        airports_data = airportsdata.load(config["airports_data"]["code"])

        messente_cfg = config["messente"]
        configuration = MessenteConfiguration(
            username=messente_cfg["public_key"], password=messente_cfg["private_key"]
        )
        messente_api = OmnimessageApi(ApiClient(configuration))
        messente_service = MessenteService(
            api=messente_api, sender=messente_cfg["sender"], to=messente_cfg["to"]
        )
        password_service = password_hash

        services = ServiceLayer(
            messente=messente_service,
            ryanair=ryanair_service,
            airports_data=airports_data,
            password_service=password_service,
        )

        loop = asyncio.get_event_loop()

        async def check_price_task(services):
            while True:
                interval = 60 * 15 # 15 minutes
                await asyncio.sleep(interval)
                check_price(services)

        loop.create_task(check_price_task(services))

        app.state.services = services

        logger.info("Finished to start-up FastAPI")

    return app
