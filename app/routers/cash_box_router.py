from fastapi import APIRouter

router = APIRouter(
    prefix="/cash_box",
    tags=["Касса"]
)


@router.get("/")
async def get_info():
    pass


@router.post("/")
async def create_recod():
    pass


@router.put("/")
async def update_record():
    pass


@router.delete("/")
async def delete_record():
    pass

