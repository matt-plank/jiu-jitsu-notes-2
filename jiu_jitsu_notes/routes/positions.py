from fastapi import Depends, HTTPException
from fastapi.requests import Request
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Position
from ..schemas import PartialPosition

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/{position_id}")
async def get_position(request: Request, position_id: int, db: Session = Depends(get_db)):
    position: Position | None = db.query(Position).filter_by(id=position_id).first()

    if position is None:
        raise HTTPException(
            status_code=404,
            detail=f"No position with id {position_id!r}",
        )

    return templates.TemplateResponse(
        "components/position/static.html",
        {
            "request": request,
            "position": position,
        },
    )


@router.put("/{position_id}")
async def update_position(
    request: Request,
    position_id: int,
    db: Session = Depends(get_db),
):
    db_position: Position | None = db.query(Position).filter_by(id=position_id).first()

    if db_position is None:
        raise HTTPException(
            status_code=404,
            detail=f"No position with id {position_id!r}",
        )

    form_data = await request.form()
    position = PartialPosition(**form_data)

    if position.name is not None:
        db_position.name = position.name

    if position.description is not None:
        db_position.description = position.description

    db.commit()

    return templates.TemplateResponse(
        "components/position/static.html",
        {
            "request": request,
            "position": db_position,
        },
    )


@router.get("/{position_id}/edit")
async def get_editable_position(request: Request, position_id: int, db: Session = Depends(get_db)):
    position: Position | None = db.query(Position).filter_by(id=position_id).first()

    if position is None:
        raise HTTPException(
            status_code=404,
            detail=f"No position with id {position_id!r}",
        )

    return templates.TemplateResponse(
        "components/position/editable.html",
        {
            "request": request,
            "position": position,
        },
    )
