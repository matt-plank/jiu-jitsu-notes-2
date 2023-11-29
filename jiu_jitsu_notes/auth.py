from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer
from passlib import hash
from sqlalchemy.orm import Session

from . import db
from .models import Token, User

MAXIMUM_TOKEN_AGE = timedelta(minutes=15)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def token_from_cookie(
    request: Request,
) -> str:
    token_string = request.cookies.get("token")

    if token_string is None:
        raise HTTPException(
            status_code=401,
            detail="No token provided",
        )

    return token_string


def current_user(
    token_string: Annotated[str, Depends(token_from_cookie)],
    session: Annotated[Session, Depends(db.get_session)],
) -> User:
    token: Token | None = db.token_from_string(session, token_string)

    if token is None or token_is_expired(token):
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    return token.user


def password_is_correct(user: User, password: str) -> bool:
    return hash.bcrypt.verify(password, user.password_hash)


def password_hash(password: str) -> str:
    return hash.bcrypt.hash(password)


def token_is_expired(token: Token) -> bool:
    """Token is expired if it is more than 15 minutes old."""
    token_age: timedelta = datetime.utcnow() - token.created_at
    return token_age > MAXIMUM_TOKEN_AGE
