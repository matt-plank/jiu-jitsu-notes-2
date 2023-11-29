from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .. import auth, db
from ..models import PositionGroup, User

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def index(
    request: Request,
):
    return templates.TemplateResponse(
        "pages/index.html",
        {
            "request": request,
        },
    )


@router.get("/groups")
async def groups_page(
    request: Request,
    session: Annotated[Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.current_user)],
):
    groups: list[PositionGroup] = db.all_groups_for_user(session, user)

    return templates.TemplateResponse(
        "pages/all_groups.html",
        {
            "request": request,
            "user": user,
            "groups": groups,
        },
    )


@router.get("/groups/{group_id}")
async def group_page(
    request: Request,
    group_id: int,
    session: Annotated[Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.current_user)],
):
    group: PositionGroup | None = db.group_by_id(session, user, group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found",
        )

    return templates.TemplateResponse(
        "pages/group.html",
        {
            "request": request,
            "group": group,
            "user": user,
        },
    )


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(
        "pages/login.html",
        {
            "request": request,
        },
    )


@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse(
        "pages/register.html",
        {
            "request": request,
        },
    )
