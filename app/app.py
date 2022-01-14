from typing import List

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database.database import get_session
from .database.models import tables
from .database.schemas import users_schemas
from .routers import routers

app = FastAPI(
    title="Shop-API",
    version="1.0.0"
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static")


@app.get("/", tags=["Главная"], response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})
    # with open("app/static/index.html", 'r') as file:
    #     content = file.read()
    # return HTMLResponse(content, status_code=200)


# For react-admin
@app.get("/users", response_model=List[users_schemas.User])
def get_user(sesiion: Session = Depends(get_session)):
    users = sesiion.query(tables.User).all()
    return users


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = "users 0-20/20"
    return response
