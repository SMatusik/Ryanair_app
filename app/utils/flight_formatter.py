import datetime
from _decimal import Decimal
from typing import List, Any

from pydantic import BaseModel


class RyanAirFlight(BaseModel):
    date: datetime.date
    time: datetime.time
    price: Decimal
    currency: str
    origin_airport_code: str
    destiny_airport_code: str
    origin_airport_name: str
    destiny_airport_name: str


class RyanAirFlightFormatter:
    def format(self, flight_data: List[Any], currency: str) -> RyanAirFlight:
        ryanair_flight = RyanAirFlight(
            date=flight_data[0].date(),
            time=flight_data[0].time(),
            price=flight_data[2],
            currency=currency,
            origin_airport_code=flight_data[3],
            origin_airport_name=flight_data[4],
            destiny_airport_code=flight_data[5],
            destiny_airport_name=flight_data[6],
        )

        return ryanair_flight