import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from utils.logger import get_logger
from utils.github_client import get_github_client
from github import GithubException # type: ignore
from nacl import public as nacl_public, encoding #type: ignore
import base64
from utils.logger import get_logger


logger = get_logger(__name__) 
g = get_github_client()

def commit_files(
    repo: str,
    file_path: str,
    commit_message: str,
    branch: str,
    content: str
):
    print(f"[github_agent] Committing changes to {repo}/{file_path} on branch '{branch}'")
    logger.info(f"[github_agent] Committing changes to {repo}/{file_path} on branch '{branch}'")

    # --- Input validation ---
    # if not repo or "/" not in repo:
    #     return "Invalid repo format. Use 'owner/repo'."
    # if not file_path or file_path.startswith(".git/"):
    #     return "Invalid file path. Must be relative to repo root and not a .git path."
    # if not commit_message.strip():
    #     return "Commit message cannot be empty."
    # if not branch.strip():
    #     return "Branch name cannot be empty."
    # if not content.strip():
    #     return "File content cannot be empty."

    try:
        # --- Validate repo exists and is accessible ---
        try:
            repository = g.get_repo(repo)
        except GithubException as e:
            if e.status == 404:
                logger.info(f"[github_agent] Repository '{repo}' not found or not accessible.")
                return f"Repository '{repo}' not found or not accessible."
            raise

        # --- Validate branch exists ---
        try:
            repository.get_branch(branch)
        except GithubException as e:
            if e.status == 404:
                # List available branches to help the agent self-correct
                available = [b.name for b in repository.get_branches()]
                logger.info(f"[github_agent] Branch '{branch}' not found. Available branches: {available}")
                return f"Branch '{branch}' not found. Available branches: {available}"
            raise

        # --- Check if file already exists (update vs create) ---
        try:
            existing_file = repository.get_contents(file_path, ref=branch)

            # File exists — check if content is actually different
            existing_content = existing_file.decoded_content.decode("utf-8")
            if existing_content == content:
                return f"No changes detected in '{file_path}'. Skipping commit."

            # Update existing file
            repository.update_file(
                path=file_path,
                message=commit_message,
                content=content,
                sha=existing_file.sha,   # required for updates
                branch=branch,
            )
            return f"File '{file_path}' updated successfully on branch '{branch}'."

        except GithubException as e:
            if e.status != 404:
                raise  # unexpected error, re-raise

            # File doesn't exist — create it
            repository.create_file(
                path=file_path,
                message=commit_message,
                content=content,
                branch=branch,
            )
            return f"File '{file_path}' created successfully on branch '{branch}'."

    except GithubException as e:
        print(f"GitHub API error [{e.status}]: {e.data}")
        return f"GitHub error {e.status}: {e.data.get('message', str(e))}"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return f"Unexpected error while committing: {str(e)}"



async def set_github_secret(repo_full_name: str, secret_name: str, secret_value: str) -> None:
    try:
        print("Repo Full Name :", repo_full_name)

        repo = g.get_repo(repo_full_name)

        # public_key = repo.get_public_key()

        # pk = nacl_public.PublicKey(
        #     public_key.key.encode(),
        #     encoding.Base64Encoder
        # )

        # box = nacl_public.SealedBox(pk)

        # encrypted_b64 = base64.b64encode(
        #     box.encrypt(secret_value.encode())
        # ).decode()

        repo.create_secret(secret_name, secret_value)

        logger.info(
            "Secret '%s' created/updated on repo %s",
            secret_name,
            repo_full_name
        )

    except Exception as e:
        logger.exception("Failed setting secret: %s", str(e))
        raise

    # except GithubException as e:
    #     logger.warning(
    #         "Failed to set secret '%s' on %s: %s",
    #         secret_name, repo_full_name, e.data
    #     )

import asyncio
if __name__ == "__main__":
    result = asyncio.run(set_github_secret("Hari-var/test_repo", "test_secret", "test_value"))
    print(result)