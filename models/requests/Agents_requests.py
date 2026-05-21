from pydantic import BaseModel
from typing import Optional

class github_agent_request(BaseModel):
    github_token: str
    prompt: str