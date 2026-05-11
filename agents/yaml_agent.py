from tools.yaml_tools.base import CI_Builder,CD_Builder,TF_Builder
from agent_framework import tool #type: ignore
from typing import Annotated
from pydantic import Field
from utils.prompt_manager_v2 import AgentDescriptionPrompt, AgentInstructionPrompt, ToolFieldsPrompt
from .BaseAgent import BaseAgent


class YamlAgent(BaseAgent):
    name = "yaml_agent"
    instructions = str(AgentInstructionPrompt("yaml-agent-instructions"))
    tools = [CI_Builder,CD_Builder,TF_Builder]

_yaml_agent_field = ToolFieldsPrompt("yaml-agent-field-description")

@tool(name="Yaml_Agent",
      description=str(AgentDescriptionPrompt("yaml-agent-description")),
      approval_mode="never_require")
async def yaml_agent(prompt: Annotated[str, Field(description = _yaml_agent_field.get("prompt"))]):
    print("called yaml agent")
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

