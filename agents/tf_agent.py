from tools.tf_tools.base import TF_Module_builder
from agent_framework import tool 
from typing import Annotated
from pydantic import Field
from utils.prompt_manager_v2 import AgentInstructionPrompt, AgentDescriptionPrompt
from .BaseAgent import BaseAgent


class TfAgent(BaseAgent):
    name = "terraform_agent"
    instructions = str(AgentInstructionPrompt("tf-agent-instructions"))
    tools=[TF_Module_builder]

@tool(name="terraform_agent",
      description=str(AgentDescriptionPrompt("tf-agent-description")),
      approval_mode="never_require")
async def terraform_agent(prompt: Annotated[str, Field(description="Full prompt including original request and any previous context")]):
    print("called terraform agent")
    return await TfAgent.get_instance().run(prompt)



