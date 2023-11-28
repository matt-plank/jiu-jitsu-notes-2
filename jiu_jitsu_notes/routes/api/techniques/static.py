from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .... import db
from ....models import Technique, User

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/{from_position_id}/techniques/{technique_id}")
async def get_single_technique(
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
            detail=f"No technique with id {technique_id!r} belongs to this position",
        )

    return templates.TemplateResponse(
        "components/technique/readonly.html",
        {
            "request": request,
            "technique": technique,
        },
    )


@router.get("/{from_position_id}/techniques/{technique_id}/detailed")
async def get_detailed_technique(
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
            detail=f"No technique with id {technique_id!r} belongs to this position",
        )

    return templates.TemplateResponse(
        "components/technique/detailed.html",
        {
            "request": request,
            "technique": technique,
        },
    )


@router.put("/{from_position_id}/techniques/{technique_id}")
async def update_single_technique(
    request: Request,
    from_position_id: int,
    technique_id: int,
    session: Annotated[Session, Depends(db.get_session)],
    user: Annotated[User, Depends(db.get_current_user)],
    name: Annotated[Optional[str], Form()] = None,
    description: Annotated[Optional[str], Form()] = None,
    to_position_id: Annotated[Optional[int], Form()] = None,
):
    db_technique: Technique | None = db.technique_by_id(session, user, technique_id)

    if db_technique is None:
        raise HTTPException(
            status_code=404,
            detail=f"No technique found with id {technique_id!r}",
        )

    if db_technique.from_position_id != from_position_id:
        raise HTTPException(
            status_code=404,
            detail=f"No technique with id {technique_id!r} belongs to this position",
        )

    if name is not None:
        db_technique.name = name

    if description is not None:
        db_technique.description = description

    if to_position_id is not None:
        db_technique.to_position_id = to_position_id

    session.commit()

    return templates.TemplateResponse(
        "components/technique/readonly.html",
        {
            "request": request,
            "technique": db_technique,
        },
    )


@router.post("/{from_position_id}/techniques/")
async def create_technique(
    request: Request,
    from_position_id: int,
    session: Annotated[Session, Depends(db.get_session)],
    user: Annotated[User, Depends(db.get_current_user)],
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    to_position_id: Annotated[Optional[int], Form()] = None,
):
    technique = db.create_technique(
        session,
        user,
        name,
        description,
        from_position_id,
        to_position_id,
    )

    return templates.TemplateResponse(
        "components/technique/readonly.html",
        {
            "request": request,
            "technique": technique,
        },
    )


@router.delete("/{from_position_id}/techniques/{technique_id}")
async def delete_technique(
    from_position_id: int,
    technique_id: int,
    session: Annotated[Session, Depends(db.get_session)],
    user: Annotated[User, Depends(db.get_current_user)],
):
    technique: Technique | None = db.technique_by_id(session, user, technique_id)

    if technique is None:
        raise HTTPException(
            status_code=404,
            detail=f"No technique with id {technique_id!r}",
        )

    if technique.from_position_id != from_position_id:
        raise HTTPException(
            status_code=404,
            detail=f"No technique with id {technique_id!r} belongs to this position",
        )

    session.delete(technique)
    session.commit()

    return Response()
