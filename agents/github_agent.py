from .BaseAgent import BaseAgent
from agent_framework import Agent #type: ignore
from agent_framework import tool #type: ignore
from typing import Annotated
from pydantic import Field
from tools.github_tools.base_trail import get_user, commit_files
from utils.prompt_manager_v2 import AgentDescriptionPrompt, AgentInstructionPrompt, ToolFieldsPrompt

class GithubAgent(BaseAgent):
    name = "github_agent"
    instructions = str(AgentInstructionPrompt("github-agent-instructions"))
    tools = [get_user, commit_files]

_git_agent_field = ToolFieldsPrompt("git-agent-field-description")

@tool(name="Github_Agent", description=str(AgentDescriptionPrompt("github-agent-description")), approval_mode="never_require")
async def github_agent(prompt: Annotated[str, Field(description = _git_agent_field.get("prompt"))]):
    print(prompt)
    return await GithubAgent.get_instance().run(prompt)

if __name__ == "__main__":
    import asyncio
    print(asyncio.run(GithubAgent.get_instance().describe_tools()))


