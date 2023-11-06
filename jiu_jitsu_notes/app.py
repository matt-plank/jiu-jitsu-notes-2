from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def get(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )
