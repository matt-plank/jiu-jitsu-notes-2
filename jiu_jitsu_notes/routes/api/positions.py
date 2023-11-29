from typing import Annotated, Literal, Optional

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ... import auth, db
from ...models import Position, PositionGroup, User

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
    session: Annotated[Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.current_user)],
):
    group: PositionGroup | None = db.group_by_id(session, user, group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found",
        )

    position: Position | None = db.position_by_id(session, user, position_id)

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
    session: Annotated[Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.current_user)],
):
    group: PositionGroup | None = db.group_by_id(session, user, group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found",
        )

    position = db.create_position_in_group(
        session,
        user,
        group,
        name=name,
        description=description,
    )

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
    session: Annotated[Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.current_user)],
):
    group: PositionGroup | None = db.group_by_id(session, user, group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found",
        )

    position: Position | None = db.position_by_id(session, user, position_id)

    if position is None or position.group_id != group_id:
        raise HTTPException(
            status_code=404,
            detail="Position not found",
        )

    if name is not None:
        position.name = name

    if description is not None:
        position.description = description

    session.commit()

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
    session: Annotated[Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.current_user)],
):
    group: PositionGroup | None = db.group_by_id(session, user, group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found",
        )

    position: Position | None = db.position_by_id(session, user, position_id)

    if position is None or position.group_id != group_id:
        raise HTTPException(
            status_code=404,
            detail="Position not found",
        )

    session.delete(position)
    session.commit()

    return Response()
