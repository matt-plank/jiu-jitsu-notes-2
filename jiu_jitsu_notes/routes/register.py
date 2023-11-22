from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def register_page(request: Request):
    return templates.TemplateResponse(
        "pages/register.html",
        {
            "request": request,
        },
    )
