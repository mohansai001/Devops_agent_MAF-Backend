from agent_framework import tool #type: ignore
from typing import Annotated
from pydantic import Field


@tool(name="CI_builder", description="Builds a CI pipeline based on the given requirements", approval_mode="never_require")
async def CI_Builder(requirements: Annotated[str, Field(description="The CI pipeline requirements")]):
    print("this is a tool for building CI pipelines")
    return ["python","fastapi"]