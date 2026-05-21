from .Base_agent import Base_Agent
from agent_framework import Agent #type: ignore
from agent_framework import tool #type: ignore
from typing import Annotated
from pydantic import Field
from tools.github_tools.base_trail import get_user, commit_files
from utils.prompt_manager_v2 import AgentDescriptionPrompt, AgentInstructionPrompt, ToolFieldsPrompt
from utils.logger import get_logger

logger = get_logger(__name__)

from dataclasses import dataclass

@dataclass
class GithubContext:
    github_pat: str

class GithubAgent(Base_Agent):   
    name = "github_agent"
    instructions = str(AgentInstructionPrompt("github-agent-instructions"))
    tools = [get_user, commit_files]

_git_agent_field = ToolFieldsPrompt("git-agent-field-description")

@tool(name="Github_Agent", description=str(AgentDescriptionPrompt("github-agent-description")), approval_mode="never_require")
async def github_agent(prompt: Annotated[str, Field(description = _git_agent_field.get("prompt"))]):
    logger.info("[github_agent] Called with prompt.")
    print("[github_agent] Called with prompt.")
    logger.debug(f"[github_agent] Prompt: {prompt}")
    print(f"[github_agent] Prompt: {prompt}")
    try:
        result = await GithubAgent.get_instance().run(prompt) #type: ignore
        logger.info("[github_agent] Successfully generated GitHub agent output.")
        print("[github_agent] Successfully generated GitHub agent output.")
        logger.debug(f"[github_agent] Output: {result}")
        print(f"[github_agent] Output: {result}")
        return result
    except Exception as e:
        logger.error(f"[github_agent] Error occurred: {e}", exc_info=True)
        print(f"[github_agent] Error occurred: {e}")
        raise

if __name__ == "__main__":
    import asyncio
    print(asyncio.run(GithubAgent.get_instance().describe_tools())) #type: ignore


