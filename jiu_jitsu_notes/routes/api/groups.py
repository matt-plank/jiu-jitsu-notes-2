from typing import Annotated, Literal, Optional

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ...db import get_db
from ...models import PositionGroup

router = APIRouter()
templates = Jinja2Templates(directory="templates")

COMPONENT_TO_TEMPLATE: dict[str, str] = {
    "list-item": "components/group/list_item/readonly.html",
    "list-item-new": "components/group/list_item/new.html",
    "header": "components/group/header/readonly.html",
    "header-editable": "components/group/header/editable.html",
}


@router.get("/")
async def get_groups(
    request: Request,
    component: Literal["list-item-new"],
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
    component: Literal["list-item", "header-editable"],
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
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    db: Annotated[Session, Depends(get_db)],
):
    if component not in COMPONENT_TO_TEMPLATE:
        raise HTTPException(
            status_code=400,
            detail="Invalid component",
        )

    db_group = PositionGroup(
        name=name,
        description=description,
    )

    db.add(db_group)
    db.commit()

    return templates.TemplateResponse(
        "components/group/list_item/readonly.html",
        {
            "request": request,
            "group": db_group,
        },
    )


@router.put("/{group_id}")
async def update_group(
    request: Request,
    group_id: int,
    name: Annotated[Optional[str], Form()],
    description: Annotated[Optional[str], Form()],
    component: Literal["header"],
    db: Annotated[Session, Depends(get_db)],
):
    db_group: PositionGroup | None = db.query(PositionGroup).get(group_id)

    if db_group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found",
        )

    if name is not None:
        db_group.name = name

    if description is not None:
        db_group.description = description

    db.commit()

    return templates.TemplateResponse(
        COMPONENT_TO_TEMPLATE[component],
        {
            "request": request,
            "group": db_group,
        },
    )


@router.delete("/{group_id}")
async def delete_group(
    group_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    group: PositionGroup | None = db.query(PositionGroup).get(group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found",
        )

    db.delete(group)
    db.commit()

    return Response(
        headers={"HX-Redirect": "/groups/"},
    )