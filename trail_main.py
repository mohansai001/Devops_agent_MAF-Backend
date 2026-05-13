import asyncio

content= """
        # Demo README

        This is a sample README file created by an automated MAF agent.

        ## Purpose
        This repository is used for testing automated GitHub operations.

        ## Notes
        - This is dummy content
        - Created for testing purposes"""

from agents.co_ordinator_agent import CoOrdinatorAgent
from agents.github_agent import GithubAgent
import asyncio
from utils.prompt_manager_v2 import TestUserPrompt
async def main():
    coordinator = CoOrdinatorAgent.get_instance()
    response = await coordinator.run(str(TestUserPrompt("CI_builder_test_prompt")))
    print(response)

asyncio.run(main())

