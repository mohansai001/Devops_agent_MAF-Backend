from utils.clientConnection import client
from agent_framework import Agent #type: ignore
from tools.yaml_tools.base import CI_Builder
from agent_framework import tool #type: ignore
from typing import Annotated
from pydantic import Field

@tool(name="YAML_Pipeline_Agent", description="An agent dedicated to build and fix yaml pipelines", approval_mode="never_require")
async def yaml_agent(prompt: Annotated[str, Field(description="The prompt to generate a YAML pipeline")]):
    print("called yaml agent")
    yaml_agent = Agent(
        client=client,
        name="yaml_agent",
        instructions="use the only the tools to help the user ",
        tools=[CI_Builder]
    )
    return await yaml_agent.run(prompt)

