from fastapi import Depends, HTTPException
from fastapi.requests import Request
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import PositionGroup

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/{group_name}")
def get_group(request: Request, group_name: str, db: Session = Depends(get_db)):
    group: PositionGroup | None = (
        db.query(PositionGroup).filter_by(name=group_name).first()
    )

    if group is None:
        raise HTTPException(
            status_code=404,
            detail=f"No group called {group_name!r}",
        )

    return templates.TemplateResponse(
        "pages/position_group.html",
        {
            "request": request,
            "group": group,
        },
    )
