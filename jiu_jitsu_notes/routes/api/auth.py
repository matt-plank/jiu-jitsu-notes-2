from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ... import auth, db
from ...models import Token, User

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/token")
async def login(
    request: Request,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: Annotated[Session, Depends(db.get_session)],
):
    user: User | None = db.user_by_email(session, email)

    if user is None or not auth.password_is_correct(user, password):
        return templates.TemplateResponse(
            "components/auth/error.html",
            {
                "request": request,
                "message": "Invalid email or password",
            },
        )

    token = db.create_token_for_user(session, user)

    response = Response()
    response.set_cookie("token", token.token)
    response.headers["hx-redirect"] = "/"

    return response


@router.delete("/token")
async def logout(
    user: Annotated[User, Depends(auth.current_user)],
    session: Annotated[Session, Depends(db.get_session)],
):
    db.delete_token_for_user(session, user)

    response = Response()
    response.delete_cookie("token")
    response.headers["hx-redirect"] = "/"

    return response


@router.post("/account")
async def create_account(
    request: Request,
    username: Annotated[str, Form()],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: Annotated[Session, Depends(db.get_session)],
):
    if db.user_by_username(session, username) is not None:
        return templates.TemplateResponse(
            "components/auth/error.html",
            {
                "request": request,
                "message": "An account with that username already exists",
            },
        )

    if db.user_by_email(session, email) is not None:
        return templates.TemplateResponse(
            "components/auth/error.html",
            {
                "request": request,
                "message": "An account with that email already exists",
            },
        )

    db.create_user(session, username, email, password)

    response = Response()
    response.headers["hx-redirect"] = "/login"

    return response
