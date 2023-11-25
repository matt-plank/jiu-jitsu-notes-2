from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.requests import Request
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ....db import get_db
from ....models import Position

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/{position_id}/editable")
async def get_editable(
    request: Request,
    position_id: int,
    db: Annotated[Session, Depends(get_db)],
):
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


@router.post("/editable")
async def new_editable(request: Request):
    return templates.TemplateResponse(
        "components/position/new.html",
        {
            "request": request,
            "group_id": request.query_params.get("groupId"),
        },
    )
