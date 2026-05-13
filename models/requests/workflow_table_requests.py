from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional

class workflow_table_requests(BaseModel):
    name: str
    type: Literal["prod","test","dev"]
    description: Optional[str] = None

class workflow_details_table_requests(BaseModel):
    workflow_id: int
    version: str
    data: Optional[dict] = None
    file_name: str
    agents: list[str]
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None