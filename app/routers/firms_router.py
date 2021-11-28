from fastapi import APIRouter

router = APIRouter(
    prefix="/firms",
    tags=["Фирмы"]
)


@router.get("/", )
async def get_fimrs():
    pass


@router.post("/")
async def create_firm():
    pass


@router.get("/{firm_id}")
async def get_firm_detail(firm_id: int):
    pass


