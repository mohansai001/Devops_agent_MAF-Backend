from pydantic import BaseModel, field_validator
from typing import Optional



class ConfigDetails(BaseModel):
    RESOURCE_GROUP: str
    LOCATION: str
    APP_NAME: str
    DEPLOY_TARGET: str
    ENVIRONMENT: str
    BRANCH: str
    ENABLE_SAST: bool
    ENABLE_DAST: bool
    APP_SERVICE_SKU: str

    @field_validator("RESOURCE_GROUP", "LOCATION", "APP_NAME", "DEPLOY_TARGET", "BRANCH", "APP_SERVICE_SKU")
    def check_non_empty(cls, v):
        if not v:
            raise ValueError("Field cannot be empty")
        return v

    @field_validator("ENABLE_SAST", "ENABLE_DAST")
    def check_boolean(cls, v):
        if not isinstance(v, bool):
            raise ValueError("Field must be a boolean")
        return v

class Techstack(BaseModel):
    language: str
    framework: str
    buildtool: str
    hasDockerfile: bool
    hasHelm: bool
    hasTerraform: bool

class ConfigValidator(BaseModel):
    config: ConfigDetails
    techstack: Techstack
    startup_command: str
    startup_command_filepath: str

