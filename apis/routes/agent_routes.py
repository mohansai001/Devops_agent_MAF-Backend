from fastapi import APIRouter #type: ignore
from agents.co_ordinator_agent import CoOrdinatorAgent
from utils.crud_ops import get_triggered_record_by_id
from database.database import db_dependency
from utils.prompt_manager_v2 import TestUserPrompt
from fastapi.responses import StreamingResponse # type: ignore
from utils.fallback_pipeline import fallback_pipeline

router = APIRouter()

@router.get("/agent/check")
async def check_agent():
    agent = CoOrdinatorAgent.get_instance()
    response = await agent.run("hi") #type: ignore
    return {"response": response}


@router.get("/agent/{id}")
async def get_agent(db:db_dependency,id: int):
    record_data = await get_triggered_record_by_id(db, id)
    if record_data is None:
        return {"error": "Record not found"}
    repo_name = record_data.repo
    branch_name = record_data.branch
    config_details = record_data.config
    techstack = record_data.techstack
    startup_command = record_data.startup_command
    startup_command_filepath = record_data.startup_command_filepath
    commit_id = record_data.commit_sha
    # agent = CoOrdinatorAgent.get_instance()
    # prompt = str(TestUserPrompt("CI_builder_test_prompt"))

    response = await fallback_pipeline(db=db, id=id) #type: ignore
    return response
    # return StreamingResponse(
    #     agent.run_stream(prompt),   # async generator
    #     media_type="text/event-stream"
    # )