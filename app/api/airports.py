from fastapi import APIRouter

from app.dependencies import dep_from_app_state, StateAttrs
from app.services import ServiceLayer


router = APIRouter()


@router.get("/airport/{airport_code}/check")
async def check_airport(
    airport_code: str, service: ServiceLayer = dep_from_app_state(StateAttrs.services)
):
    return service.airports_data.get(airport_code)


@router.get("/country/{country_code}/check")
async def check_country_airports(
    country_code: str, service: ServiceLayer = dep_from_app_state(StateAttrs.services)
):
    airports = []
    for airport in service.airports_data:

        if service.airports_data[airport]["country"] == country_code:
            airports.append(service.airports_data[airport])

    return airports
