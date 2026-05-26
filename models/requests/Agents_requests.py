from pydantic import BaseModel
from typing import Optional

class github_agent_request(BaseModel):
    prompt: str

class yaml_agent_request(BaseModel):
    prompt: str

class terraform_agent_request(BaseModel):
    prompt: str

