from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ...db import get_db
from ...models import Position, Technique

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/{from_position_id}/techniques/{technique_id}/editable")
async def get_editable_for_position(
    request: Request,
    from_position_id: int,
    technique_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    technique: Technique | None = db.query(Technique).filter_by(id=technique_id).first()

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
            "positions": db.query(Position).all(),
        },
    )


@router.post("/{from_position_id}/techniques/editable")
async def create_editable(
    request: Request,
    from_position_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    return templates.TemplateResponse(
        "components/technique/new.html",
        {
            "request": request,
            "from_position_id": from_position_id,
            "positions": db.query(Position).all(),
        },
    )
