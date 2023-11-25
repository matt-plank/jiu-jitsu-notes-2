from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .. import schemas
from ..db import get_db
from ..models import PositionGroup

router = APIRouter()
templates = Jinja2Templates(directory="templates")

COMPONENT_TO_TEMPLATE: dict[str, str] = {
    "list-item": "components/group/static.html",
    "list-item-new": "components/group/new.html",
}


@router.get("/")
async def get_groups(
    request: Request,
    component: Literal["list-item", "list-item-new"],
    db: Annotated[Session, Depends(get_db)],
):
    if component not in COMPONENT_TO_TEMPLATE:
        raise HTTPException(
            status_code=400,
            detail="Invalid component",
        )

    groups: list[PositionGroup] = db.query(PositionGroup).all()

    return templates.TemplateResponse(
        COMPONENT_TO_TEMPLATE[component],
        {
            "request": request,
            "groups": groups,
        },
    )


@router.get("/{group_id}")
async def get_group(
    request: Request,
    group_id: int,
    component: Literal["list-item"],
    db: Annotated[Session, Depends(get_db)],
):
    if component not in COMPONENT_TO_TEMPLATE:
        raise HTTPException(
            status_code=400,
            detail="Invalid component",
        )

    group: PositionGroup | None = db.query(PositionGroup).get(group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found",
        )

    return templates.TemplateResponse(
        COMPONENT_TO_TEMPLATE[component],
        {
            "request": request,
            "group": group,
        },
    )


@router.post("/")
async def create_group(
    request: Request,
    component: Literal["list-item"],
    db: Annotated[Session, Depends(get_db)],
):
    if component not in COMPONENT_TO_TEMPLATE:
        raise HTTPException(
            status_code=400,
            detail="Invalid component",
        )

    form_data = await request.form()
    group = schemas.NewGroup(**form_data)  # type: ignore
    db_group = PositionGroup(**group.model_dump())

    db.add(db_group)
    db.commit()

    return templates.TemplateResponse(
        "components/group/static.html",
        {
            "request": request,
            "group": db_group,
        },
    )
