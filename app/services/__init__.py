from dataclasses import dataclass
from typing import Dict, Any

from app.services.messente import MessenteService
from app.services.ryanair import RyanAirService
from app.utils.password_hash import PasswordHash


@dataclass
class ServiceLayer:
    ryanair: RyanAirService
    messente: MessenteService
    airports_data: Dict[str, Any]
    password_service: PasswordHash
