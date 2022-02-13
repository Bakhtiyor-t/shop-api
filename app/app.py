from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.metadata import api_description, api_version, api_title, api_contacts, tags_metadata
from .routers import routers

app = FastAPI(
    title=api_title,
    version=api_version,
    description=api_description,
    contact=api_contacts,
    openapi_tags=tags_metadata
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


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    # headers for react admin
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = "users 0-20/20"
    return response
