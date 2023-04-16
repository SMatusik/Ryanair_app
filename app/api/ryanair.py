from datetime import datetime
from typing import Optional

from fastapi import APIRouter

from app.dependencies import dep_from_app_state, StateAttrs
from app.enums import CURRENCIES
from app.services import ServiceLayer
from app.tasks.ryanair_tasks import check_price
from app.utils.flight_formatter import RyanAirFlightFormatter

router = APIRouter()


@router.get("/")
async def check_for_flight(
    service: ServiceLayer = dep_from_app_state(StateAttrs.services),
):
    price = check_price(service, 1)

    return {"price": price}


@router.get("/{origin_airport_code}/flights")
async def check_for_flights_from(
    origin_airport_code: str,
    start_date: datetime,
    end_date: datetime,
    destination_country: Optional[str] = None,
    service: ServiceLayer = dep_from_app_state(StateAttrs.services),
):
    currency = CURRENCIES.PLN
    if not service.airports_data.get(origin_airport_code):
        return {"error": "airport does not exists"}

    if start_date.date() < datetime.today().date():
        return {"error": "date cannot be in past"}

    flights = service.ryanair.check_flights_from(
        airport_code=origin_airport_code,
        start_date=start_date,
        end_date=end_date,
        currency=currency,
        destination_country=destination_country,
    )
    ryanair_flights = [RyanAirFlightFormatter().format(flight, currency) for flight in flights]
    return {"flights": ryanair_flights}
