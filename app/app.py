from fastapi import FastAPI

from .routers import routers

app = FastAPI()
app.include_router(routers.router)


@app.get("/")
def index():
    return {"message": "This Home page"}
