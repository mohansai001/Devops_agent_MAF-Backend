from fastapi import APIRouter, Header, HTTPException, Depends #type: ignore
from agents.co_ordinator_agent import CoOrdinatorAgent
from utils.crud_ops import get_triggered_record_by_id
from database.database import db_dependency
from utils.prompt_manager_v2 import TestUserPrompt
from fastapi.responses import StreamingResponse # type: ignore
from utils.fallback_pipeline import fallback_pipeline
from models.requests.Agents_requests import github_agent_request, yaml_agent_request, terraform_agent_request
from agents.github_agent import github_agent
from agents.yaml_agent import yaml_agent
from utils.request_context import github_pat_ctx

router = APIRouter()

@router.get("/agent/check")
async def check_agent():
    agent = CoOrdinatorAgent.get_instance()
    response = await agent.run("hi") #type: ignore
    return {"response": response}


@router.get("/agent/{id}")
async def get_agent(db:db_dependency,id: int):
    # record_data = await get_triggered_record_by_id(db, id)
    # if record_data is None:
    #     return {"error": "Record not found"}
    # repo_name = record_data.repo
    # branch_name = record_data.branch
    # config_details = record_data.config
    # techstack = record_data.techstack
    # startup_command = record_data.startup_command
    # startup_command_filepath = record_data.startup_command_filepath
    # commit_id = record_data.commit_sha
    # agent = CoOrdinatorAgent.get_instance()
    # prompt = str(TestUserPrompt("CI_builder_test_prompt"))

    response = await fallback_pipeline(db=db, id=id) #type: ignore
    return response
    # return StreamingResponse(
    #     agent.run_stream(prompt),   # async generator
    #     media_type="text/event-stream"
    # )

@router.get("/agent/{id}")
async def co_ordinator_agent_call(db:db_dependency,id: int):
    record_data = await get_triggered_record_by_id(db, id)
    if record_data is None:
        return {"error": "Record not found"}
    # repo_name = record_data.repo
    # branch_name = record_data.branch
    # config_details = record_data.config
    # techstack = record_data.techstack
    # startup_command = record_data.startup_command
    # startup_command_filepath = record_data.startup_command_filepath
    # commit_id = record_data.commit_sha
    agent = CoOrdinatorAgent.get_instance()
    prompt = str(TestUserPrompt("CI_builder_test_prompt"))
    response = await agent.run(prompt) #type: ignore
    # response = await fallback_pipeline(db=db, id=id) #type: ignore
    return response
    # return StreamingResponse(
    #     agent.run_stream(prompt),   # async generator
    #     media_type="text/event-stream"
    # )
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials #type: ignore

security = HTTPBearer()

@router.post("/github_agent")
async def github_agent_call(request: github_agent_request, authorization: HTTPAuthorizationCredentials = Depends(security)):
    print("SCHEME:", authorization.scheme)
    print("AUTH:", authorization.credentials)

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing token"
        )
    git_token = authorization.credentials #.replace("Bearer ", "")
    print(f"Token received: {git_token}")
    prompt = request.prompt

    token_ref = github_pat_ctx.set(git_token)

    try:
        response = await github_agent(prompt)

        return {
            "response": f"Github agent executed successfully",
            "agent_output": response
        }

    finally:
        github_pat_ctx.reset(token_ref)

@router.post("/yaml_agent")
async def yaml_agent_call(request: yaml_agent_request, authorization: HTTPAuthorizationCredentials = Depends(security)):
    print("SCHEME:", authorization.scheme)
    print("AUTH:", authorization.credentials)

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing token"
        )
    git_token = authorization.credentials #.replace("Bearer ", "")
    print(f"Token received: {git_token}")
    prompt = request.prompt

    token_ref = github_pat_ctx.set(git_token)

    try:
        response = await yaml_agent(prompt)
        print(f"YAML AGENT RESPONSE: {response}")

        return {
            "response": f"YAML agent executed successfully",
            "agent_output": response
        }

    finally:
        github_pat_ctx.reset(token_ref)