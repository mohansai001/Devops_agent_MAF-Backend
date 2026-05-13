from fastapi import APIRouter #type: ignore
from database.database import db_dependency
from utils.crud_ops import get_all_triggered_records, get_agents, add_agent, get_workflows, push_workflow_record, push_workflow_details_record
from models.requests.Agents_table_requests import AgentCreateRequest
from models.requests.workflow_table_requests import workflow_table_requests, workflow_details_table_requests

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

@router.get("/get_workflows")
async def get_workflow(db: db_dependency):
    return await get_workflows(db)

@router.post("/push_workflow")
async def push_workflow(db: db_dependency, workflow: workflow_table_requests):
    return await push_workflow_record(db, workflow)

@router.post("/push_workflow_details")
async def push_workflow_details(db: db_dependency, workflow_details: workflow_details_table_requests):
    return await push_workflow_details_record(db, workflow_details)
