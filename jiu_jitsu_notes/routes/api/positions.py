from typing import Annotated, Literal, Optional

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ...db import get_db
from ...models import Position, PositionGroup

router = APIRouter()
templates = Jinja2Templates(directory="templates")


COMPONENT_TO_TEMPLATE: dict[str, str] = {
    "list": "components/position/list_item/list.html",
    "list-item": "components/position/list_item/readonly.html",
    "list-item-editable": "components/position/list_item/editable.html",
    "list-item-new": "components/position/list_item/new.html",
}


@router.get("/groups/{group_id}/positions")
async def get_all_positions(
    request: Request,
    group_id: int,
    component: Literal["list", "list-item-new"],
    db: Annotated[Session, Depends(get_db)],
):
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


@router.get("/groups/{group_id}/positions/{position_id}")
async def get_position(
    request: Request,
    group_id: int,
    position_id: int,
    component: Literal["list-item", "list-item-editable"],
    db: Annotated[Session, Depends(get_db)],
):
    group: PositionGroup | None = db.query(PositionGroup).get(group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found",
        )

    position: Position | None = db.query(Position).get(position_id)

    if position is None or position.group_id != group_id:
        raise HTTPException(
            status_code=404,
            detail="Position not found",
        )

    return templates.TemplateResponse(
        COMPONENT_TO_TEMPLATE[component],
        {
            "request": request,
            "group": group,
            "position": position,
        },
    )


@router.post("/groups/{group_id}/positions/")
async def create_position_in_group(
    request: Request,
    group_id: int,
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    component: Literal["list-item"],
    db: Annotated[Session, Depends(get_db)],
):
    group: PositionGroup | None = db.query(PositionGroup).get(group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found",
        )

    position = Position(
        name=name,
        description=description,
        group_id=group_id,
    )

    db.add(position)
    db.commit()

    return templates.TemplateResponse(
        COMPONENT_TO_TEMPLATE[component],
        {
            "request": request,
            "group": group,
            "position": position,
        },
    )


@router.put("/groups/{group_id}/positions/{position_id}")
async def update_position(
    request: Request,
    group_id: int,
    position_id: int,
    name: Annotated[Optional[str], Form()],
    description: Annotated[Optional[str], Form()],
    component: Literal["list-item"],
    db: Annotated[Session, Depends(get_db)],
):
    group: PositionGroup | None = db.query(PositionGroup).get(group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found",
        )

    position: Position | None = db.query(Position).get(position_id)

    if position is None or position.group_id != group_id:
        raise HTTPException(
            status_code=404,
            detail="Position not found",
        )

    if name is not None:
        position.name = name

    if description is not None:
        position.description = description

    db.commit()

    return templates.TemplateResponse(
        COMPONENT_TO_TEMPLATE[component],
        {
            "request": request,
            "group": group,
            "position": position,
        },
    )


@router.delete("/groups/{group_id}/positions/{position_id}")
async def delete_position(
    group_id: int,
    position_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    group: PositionGroup | None = db.query(PositionGroup).get(group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found",
        )

    position: Position | None = db.query(Position).get(position_id)

    if position is None or position.group_id != group_id:
        raise HTTPException(
            status_code=404,
            detail="Position not found",
        )

    db.delete(position)
    db.commit()

    return Response()
