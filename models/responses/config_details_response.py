from pydantic import BaseModel
from typing import Literal
from datetime import datetime
from typing import Optional
from models.validators.config_validator_model import ConfigDetails, Techstack


class ConfigDetailsRequest(BaseModel):
    id: int
    repo: str
    branch: str
    commit_sha: str
    commit_message: str
    committed_by: str
    committed_at: datetime
    changed_files: list
    config: ConfigDetails
    techstack: Techstack
    status: Literal['pending', 'approved']
    startup_command: Optional[str] = None
    startup_command_filepath: Optional[str] = None
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None
