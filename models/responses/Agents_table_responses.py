from pydantic import BaseModel
from datetime import datetime

class AgentResponse(BaseModel):
    id: int
    name: str
    status: str
    created_at: datetime
    created_by: str
    wrapper_prompt_path: str
    required_fields: dict
    updated_at: datetime
    updated_by: str