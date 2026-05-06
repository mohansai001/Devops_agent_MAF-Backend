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

async def main():
    coordinator = CoOrdinatorAgent.get_instance()
    response = await coordinator.run(f"""add a new README file to a repository.

        Details:
        - Repository: Hari-var/test_repo
        - Branch: feature/add-readme
        - File path: docs/README.md
        - Commit message: "Add README with given content"

        - content: {content}

        - Instructions:
        1. Create a new branch from main called "feature/add-readme" if it does not exist.
        2. Add the file at the specified path.
        3. Commit the file with the given message.
        4. Do not modify any other files.
        5. Use the appropriate tool to push the file to the repository.""")
    print(response)

asyncio.run(main())

