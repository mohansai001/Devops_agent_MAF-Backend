
from utils.config import github_token
from agent_framework import tool #type: ignore
from github import Github, Auth, GithubException # type: ignore
from typing import Annotated
from pydantic import Field
from utils.prompt_manager_v2 import ToolDescriptionPrompt
from utils.prompt_manager_v2 import ToolFieldsPrompt


def get_github_client():
    auth = Auth.Token(github_token)
    return Github(auth=auth)

@tool(name="get_user", description=str(ToolDescriptionPrompt("git-get-user-tool-description")), approval_mode="never_require")
def get_user():
    print("github_token:", github_token)
    g_client = get_github_client()
    user = g_client.get_user()
    print("login:", user.login)
    print("type:", type(user))
    print(user)
    return user

_git_commit_fields = ToolFieldsPrompt("git-commit-field-description")

@tool(
    name="commit_files",
    description=str(ToolDescriptionPrompt("git-commit-tool-description")),
    approval_mode="never_required"
)
def commit_changes(
    repo: Annotated[str, Field(description = _git_commit_fields.get("repo"))],
    file_path: Annotated[str, Field(description = _git_commit_fields.get("file_path"))],
    commit_message: Annotated[str, Field(description = _git_commit_fields.get("commit_message"))],
    branch: Annotated[str, Field(description = _git_commit_fields.get("branch"))],
    content: Annotated[str, Field(description = _git_commit_fields.get("content"))]
):
    print(f"Committing changes to {repo}/{file_path} on branch '{branch}'")

    # --- Input validation ---
    if not repo or "/" not in repo:
        return "Invalid repo format. Use 'owner/repo'."
    if not file_path or file_path.startswith(".git"):
        return "Invalid file path. Must be relative to repo root and not a .git path."
    if not commit_message.strip():
        return "Commit message cannot be empty."
    if not branch.strip():
        return "Branch name cannot be empty."
    if not content.strip():
        return "File content cannot be empty."

    try:
        g_client = get_github_client()

        # --- Validate repo exists and is accessible ---
        try:
            repository = g_client.get_repo(repo)
        except GithubException as e:
            if e.status == 404:
                return f"Repository '{repo}' not found or not accessible."
            raise

        # --- Validate branch exists ---
        try:
            repository.get_branch(branch)
        except GithubException as e:
            if e.status == 404:
                # List available branches to help the agent self-correct
                available = [b.name for b in repository.get_branches()]
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
    
if __name__ == "__main__":
    commit_changes(repo="Hari-var/test_repo", file_path="docs/README.md", commit_message="Add README with dummy content", branch="feature/add-readme", content="# Demo README\n\nThis is a sample README file created by an automated MAF agent.\n\n## Purpose\nThis repository is used for testing automated GitHub operations.\n\n## Notes\n- This is dummy content\n- Created for testing purposes")
