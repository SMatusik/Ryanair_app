import logging
from enum import Enum
from typing import Any, Optional

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from requests import Session
from starlette.requests import Request

from app.db import database
from app.db.models.users import User
from app.utils.password_hash import password_hash

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)
import logging

logger = logging.getLogger(__name__)
class StateAttrs(Enum):
    services = "services"
    airports_data = "airports_data"
    password_service = "password_service"


def dep_from_app_state(name: StateAttrs) -> Any:
    def inner(request: Request) -> Any:
        return getattr(request.app.state, name.name)

    return Depends(inner)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)) -> Optional[User]:
    try:
        logger.error(token)
        payload = password_hash.decode_access_token(token)
        logger.error(f"{payload =}")

        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user