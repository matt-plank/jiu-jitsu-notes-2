from fastapi import Depends
from fastapi.requests import Request
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ... import schemas
from ...db import get_db
from ...models import PositionGroup

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/list")
async def create_filtered_list_list(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()

    group_query = db.query(PositionGroup)

    if "search" in form_data:
        search_query: str = form_data["search"]  # type: ignore
        group_query = group_query.filter(
            PositionGroup.name.contains(search_query),
        )

    groups = group_query.all()

    return templates.TemplateResponse(
        "components/group/list.html",
        {
            "request": request,
            "groups": groups,
        },
    )


@router.post("/")
async def create_group(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    group = schemas.NewGroup(**form_data)  # type: ignore
    db_group = PositionGroup(**group.model_dump())

    db.add(db_group)
    db.commit()

    return templates.TemplateResponse(
        "components/group/static.html",
        {
            "request": request,
            "group": db_group,
        },
    )
