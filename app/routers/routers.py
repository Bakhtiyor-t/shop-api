from fastapi import APIRouter
from . import \
    auth_router, \
    cash_box_router, \
    debtors_router, \
    expenses_router, \
    firms_router, \
    shopping_list_router, \
    main_router

router = APIRouter()

router.include_router(auth_router.router)
router.include_router(cash_box_router.router)
router.include_router(debtors_router.router)
router.include_router(expenses_router.router)
router.include_router(firms_router.router)
router.include_router(shopping_list_router.router)
router.include_router(main_router.router)
