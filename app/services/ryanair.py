from datetime import datetime
from dataclasses import dataclass
from typing import Optional

from ryanair import Ryanair


@dataclass
class RyanAirService:
    api: Ryanair
    threshold: float

    def check_flight(
        self,
        departure_airport: str = "TSF",
        destination_airport: str = "POZ",
        date: Optional[datetime] = None,
    ) -> float:
        if not date:
            return 0.0

        flights = self.api.get_all_flights(departure_airport, date, destination_airport)

        if len(flights) > 0:
            return flights[0].price

    def check_if_flight_is_cheaper(self, price: float):
        return price < self.threshold

    def check_flights_from(
        self,
        airport_code: str,
        start_date: datetime,
        end_date: datetime,
        currency: str,
        destination_country: Optional[str] = None,
    ):
        self.api.currency = currency
        return self.api.get_cheapest_flights(
            airport=airport_code,
            date_from=start_date,
            date_to=end_date,
            destination_country=destination_country,
        )
