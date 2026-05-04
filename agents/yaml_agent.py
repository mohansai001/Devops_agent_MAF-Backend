from tools.yaml_tools.base import CI_Builder
from agent_framework import tool #type: ignore
from typing import Annotated
from pydantic import Field
from utils.prompt_manager import PromptManager
from .BaseAgent import BaseAgent


class YamlAgent(BaseAgent):
    name = "yaml_agent"
    instructions = PromptManager().format("yaml-agent-instructions")
    tools = [CI_Builder]

@tool(name="Yaml_Agent",
      description="An agent dedicated to YAML responsibilities",
      approval_mode="never_require")
async def yaml_agent(prompt: Annotated[str, Field(description="Full prompt including original request and any previous context")]):
    return await YamlAgent.get_instance().run(prompt)


# @tool(name="YAML_Pipeline_Agent", description="An agent dedicated to build and fix yaml pipelines", approval_mode="never_require")
# async def yaml_agent(prompt: Annotated[str, Field(description="The prompt to generate a YAML pipeline")]):
#     print("called yaml agent")
#     yaml_agent = Agent(
#         client=client,
#         name="yaml_agent",
#         instructions= PromptManager().format("yaml_agent_instructions"),
#         tools=[CI_Builder]
#     )
#     return await yaml_agent.run(prompt)

