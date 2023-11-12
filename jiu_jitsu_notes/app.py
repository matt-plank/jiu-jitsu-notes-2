from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .db import engine
from .models import Base
from .routes import groups, positions, techniques

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(groups.router, prefix="/groups")
app.include_router(positions.router, prefix="/positions")
app.include_router(techniques.router, prefix="/techniques")

app.mount("/css", StaticFiles(directory="templates/css"), name="static")

templates = Jinja2Templates(directory="templates")
