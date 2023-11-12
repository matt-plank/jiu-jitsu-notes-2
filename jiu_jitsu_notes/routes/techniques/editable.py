from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ...db import get_db
from ...models import Position, Technique

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/{technique_id}/editable")
async def get_editable_for_position(
    request: Request,
    technique_id: int,
    db: Session = Depends(get_db),
):
    technique: Technique | None = db.query(Technique).filter_by(id=technique_id).first()

    if technique is None:
        raise HTTPException(
            status_code=404,
            detail=f"No technique found with id {technique_id!r}",
        )

    return templates.TemplateResponse(
        "components/technique/editable.html",
        {
            "request": request,
            "technique": technique,
            "positions": db.query(Position).all(),
        },
    )


@router.post("/editable")
async def create_editable(
    request: Request,
    fromPositionId: int,
    db: Session = Depends(get_db),
):
    return templates.TemplateResponse(
        "components/technique/new.html",
        {
            "request": request,
            "from_position_id": fromPositionId,
            "positions": db.query(Position).all(),
        },
    )
