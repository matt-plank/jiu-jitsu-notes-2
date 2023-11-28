from typing import Annotated, Literal, Optional

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ... import db
from ...models import PositionGroup, User

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
    session: Annotated[Session, Depends(db.get_session)],
    user: Annotated[User, Depends(db.get_current_user)],
):
    if component not in COMPONENT_TO_TEMPLATE:
        raise HTTPException(
            status_code=400,
            detail="Invalid component",
        )

    groups: list[PositionGroup] = db.all_groups_for_user(session, user)

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
    session: Annotated[Session, Depends(db.get_session)],
    user: Annotated[User, Depends(db.get_current_user)],
):
    if component not in COMPONENT_TO_TEMPLATE:
        raise HTTPException(
            status_code=400,
            detail="Invalid component",
        )

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


@router.post("/")
async def create_group(
    request: Request,
    component: Literal["list-item"],
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    session: Annotated[Session, Depends(db.get_session)],
    user: Annotated[User, Depends(db.get_current_user)],
):
    if component not in COMPONENT_TO_TEMPLATE:
        raise HTTPException(
            status_code=400,
            detail="Invalid component",
        )

    db_group = db.create_group(session, user, name, description)

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
    session: Annotated[Session, Depends(db.get_session)],
    user: Annotated[User, Depends(db.get_current_user)],
):
    group: PositionGroup | None = db.group_by_id(session, user, group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found",
        )

    group = db.update_group(session, group, name, description)

    return templates.TemplateResponse(
        COMPONENT_TO_TEMPLATE[component],
        {
            "request": request,
            "group": group,
        },
    )


@router.delete("/{group_id}")
async def delete_group(
    group_id: int,
    session: Annotated[Session, Depends(db.get_session)],
    user: Annotated[User, Depends(db.get_current_user)],
):
    group: PositionGroup | None = db.group_by_id(session, user, group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found",
        )

    session.delete(group)
    session.commit()

    return Response(
        headers={"HX-Redirect": "/groups/"},
    )
