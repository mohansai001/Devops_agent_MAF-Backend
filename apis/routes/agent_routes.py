from fastapi import APIRouter #type: ignore
from agents.co_ordinator_agent import CoOrdinatorAgent
from utils.crud_ops import get_triggered_record_by_id
from database.database import db_dependency

router = APIRouter()

@router.get("/agent/{id}")
async def get_agent(db:db_dependency,id: int):
    record_data = await get_triggered_record_by_id(db, id)
    if record_data is None:
        return {"error": "Record not found"}
    config_details = record_data.config
    techstack = record_data.techstack
    startup_command = record_data.startup_command
    startup_command_filepath = record_data.startup_command_filepath
    # agent = CoOrdinatorAgent.get_instance()
    return {"config_details": config_details, 
            "techstack": techstack, 
            "startup_command": startup_command, 
            "startup_command_filepath": startup_command_filepath}
