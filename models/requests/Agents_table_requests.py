from pydantic import BaseModel
from datetime import datetime

class AgentCreateRequest(BaseModel):
    agent_name: str
    created_by: str
    created_at: datetime

class AgentUpdateRequest(BaseModel):
    agent_name: str
    updated_by: str
    updated_at: datetime