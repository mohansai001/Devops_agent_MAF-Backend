from pydantic import BaseModel
from datetime import datetime

class AgentResponse(BaseModel):
    id: int
    name: str
    status: str
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str