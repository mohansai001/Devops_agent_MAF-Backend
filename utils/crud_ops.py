import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy.orm import Session, selectinload
from database.database import sessionlocal
from models.tables.config_details import ConfigDetails
from models.tables.Agents import Agents
from models.tables.workflows import Workflow, WorkflowDetails
from models.requests.workflow_table_requests import workflow_table_requests, workflow_details_table_requests
from models.requests.Agents_table_requests import AgentCreateRequest, AgentUpdateRequest
from models.responses.Agents_table_responses import AgentResponse
from models.responses.config_details_response import ConfigDetailsRequest
from typing import Union


async def get_all_triggered_records(db: Session) :
    result = db.query(ConfigDetails).all()
    if not result:
        return None
    return [item for item in result]

class AgentOps:
    pass

async def get_triggered_record_by_id(db: Session, record_id: int) -> Union[ConfigDetails, None]:
    return db.query(ConfigDetails).filter(ConfigDetails.id == record_id).first()

async def get_agents(db: Session):
    return db.query(Agents).all()

async def add_agent(db:Session, details:AgentCreateRequest) -> Agents:
    new_agent = Agents(
        agent_name=details.agent_name,
        created_by=details.created_by,
        created_at=details.created_at
    )
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)
    return new_agent

async def update_agent(db:Session, agent_id:int, details:AgentUpdateRequest) -> Union[Agents, None]:
    agent = db.query(Agents).filter(Agents.id == agent_id).first()
    if not agent:
        return None
    agent.agent_name = details.agent_name
    agent.updated_by = details.updated_by
    agent.updated_at = details.updated_at
    db.commit()
    db.refresh(agent)
    return agent

async def get_workflows(db: Session):
    return (
        db.query(Workflow)
        .options(selectinload(Workflow.details))
        .all()
    )

async def push_workflow_record(db: Session, workflow: workflow_table_requests):
    details = Workflow(**workflow.model_dump())
    db.add(details)
    db.commit()
    db.refresh(details)
    return details

async def push_workflow_details_record(db: Session,workflow_details:workflow_details_table_requests):
    details = WorkflowDetails(**workflow_details.model_dump())
    db.add(details)
    db.commit()
    db.refresh(details)
    return details


import asyncio

if __name__ == "__main__":
    db = sessionlocal()
    result = asyncio.run(get_workflows(db=db))
    print(result)