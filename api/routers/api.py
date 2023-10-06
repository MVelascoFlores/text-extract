from fastapi import APIRouter

from api.routers import (
    llm, 
    user,
)


router = APIRouter()

router.include_router(
    llm.router, prefix="/llm", tags=['Llm'],
)
router.include_router(
    user.router, prefix="/user", tags=['User'],
)
