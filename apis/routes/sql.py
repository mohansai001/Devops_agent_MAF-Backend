from fastapi import APIRouter #type: ignore
from database.database import db_dependency
from utils.crud_ops import get_all_triggered_records, get_agents, add_agent
from models.requests.Agents_table_requests import AgentCreateRequest

router = APIRouter(prefix="/sql", tags=["SQL"])

@router.get("/get_all_triggered_records")
async def get_all_triggered(db: db_dependency):
    return await get_all_triggered_records(db)

@router.get("/get_available_agents")
async def get_all_agents(db: db_dependency):
    return await get_agents(db)

@router.post("/add_agent")
async def create_agent(db: db_dependency, details: AgentCreateRequest):
    return await add_agent(db, details)