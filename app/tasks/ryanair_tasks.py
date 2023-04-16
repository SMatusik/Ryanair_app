from datetime import datetime
import logging
from app.services import ServiceLayer

logger = logging.getLogger(__name__)


def check_price(service: ServiceLayer) -> float:
    date = datetime(year=2023, month=5, day=9)
    price = service.ryanair.check_flight(date=date)

    if service.ryanair.check_if_flight_is_cheaper(price=price):
        # service.messente.send_alert(price)
        pass

    logging.info(f"{datetime.now()} - price is {price} EUR")

    return price
