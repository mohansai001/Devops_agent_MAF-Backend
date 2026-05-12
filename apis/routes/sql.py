from fastapi import APIRouter #type: ignore
from database.database import db_dependency
from utils.crud_ops import get_all_triggered_records

router = APIRouter(prefix="/sql", tags=["SQL"])

@router.get("/get_all_triggered_records")
async def get_all_triggered(db: db_dependency):
    return await get_all_triggered_records(db)


