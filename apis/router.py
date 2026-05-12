from fastapi import APIRouter #type: ignore
from .routes.sql import router as sql_router

router = APIRouter()

router.include_router(sql_router,tags=["SQL"],prefix="/sql")
