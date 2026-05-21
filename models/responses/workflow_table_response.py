from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal


class WorkflowTableResponse(BaseModel):
    id: int
    name: str
    type: Literal["prod","test","dev"]
    description: Optional[str] = None

class WorkflowDetailsTableResponse(BaseModel):
    id: int
    workflow_id: int
    version: str
    data: Optional[dict] = None
    file_name: str
    agents: list[str]
    task_sequence: list[str]
    run_logs: dict
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None


class WorkflowResponse(BaseModel):
    id: int
    name: str
    type: str
    details: list[WorkflowDetailsTableResponse]