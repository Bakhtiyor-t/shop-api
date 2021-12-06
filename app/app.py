from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .routers import routers

app = FastAPI(
    title="Shop-API",
    version="1.0.0"
)
app.include_router(routers.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/static")


@app.get("/", tags=["Главная"], response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})
    # with open("app/static/index.html", 'r') as file:
    #     content = file.read()
    # return HTMLResponse(content, status_code=200)
