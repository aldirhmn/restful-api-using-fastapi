from fastapi import APIRouter
# from endpoints import product, user
from endpoint import product, user, users

router = APIRouter()
router.include_router(product.router)
router.include_router(user.router)
router.include_router(users.router)