from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import PositionGroup

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "pages/index.html",
        {
            "request": request,
        },
    )


@router.get("/groups")
async def groups_page(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
):
    groups: list[PositionGroup] = db.query(PositionGroup).all()

    return templates.TemplateResponse(
        "pages/all_groups.html",
        {
            "request": request,
            "groups": groups,
        },
    )


@router.get("/groups/{group_id}")
async def group_page(
    request: Request,
    group_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    group: list[PositionGroup] | None = db.query(PositionGroup).get(group_id)

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


@router.get("/")
async def register_page(request: Request):
    return templates.TemplateResponse(
        "pages/register.html",
        {
            "request": request,
        },
    )
