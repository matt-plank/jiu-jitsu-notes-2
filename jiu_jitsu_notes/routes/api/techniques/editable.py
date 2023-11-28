from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .... import db
from ....models import Position, Technique, User

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/{from_position_id}/techniques/{technique_id}/editable")
async def get_editable_for_position(
    request: Request,
    from_position_id: int,
    technique_id: int,
    session: Annotated[Session, Depends(db.get_session)],
    user: Annotated[User, Depends(db.get_current_user)],
):
    technique: Technique | None = db.technique_by_id(session, user, technique_id)

    if technique is None:
        raise HTTPException(
            status_code=404,
            detail=f"No technique found with id {technique_id!r}",
        )

    if technique.from_position_id != from_position_id:
        raise HTTPException(
            status_code=404,
            detail=f"The technique with id {technique_id!r} does not belong to this position",
        )

    return templates.TemplateResponse(
        "components/technique/editable.html",
        {
            "request": request,
            "technique": technique,
            "positions": db.all_positions_for_user(session, user),
        },
    )


@router.post("/{from_position_id}/techniques/editable")
async def create_editable(
    request: Request,
    from_position_id: int,
    session: Annotated[Session, Depends(db.get_session)],
    user: Annotated[User, Depends(db.get_current_user)],
):
    return templates.TemplateResponse(
        "components/technique/new.html",
        {
            "request": request,
            "from_position_id": from_position_id,
            "positions": db.all_positions_for_user(session, user),
        },
    )
