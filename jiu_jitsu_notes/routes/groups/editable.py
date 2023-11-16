from fastapi.requests import Request
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/editable")
async def create_group_editable(request: Request):
    return templates.TemplateResponse(
        "components/group/new.html",
        {
            "request": request,
        },
    )
