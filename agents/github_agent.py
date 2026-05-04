from .BaseAgent import BaseAgent
from agent_framework import Agent #type: ignore
from agent_framework import tool #type: ignore
from typing import Annotated
from pydantic import Field
from tools.github_tools.base_trail import get_user, commit_changes
from utils.prompt_manager import PromptManager

class GithubAgent(BaseAgent):
    name = "github_agent"
    instructions = PromptManager().format("github-agent-instructions")
    tools = [get_user, commit_changes]

@tool(name="Github_Agent", description="An agent dedicated to git responsibilities", approval_mode="never_require")
async def github_agent(prompt: Annotated[str, Field(description="The prompt to generate a GitHub action")]):
    return await GithubAgent.get_instance().run(prompt)


