from agent_framework import tool #type: ignore
from typing import Annotated
from pydantic import Field
from utils.prompt_manager_v2 import ToolDescriptionPrompt
from utils.prompt_manager_v2 import ToolFieldsPrompt
from utils.github_client import get_github_client
from adapters.github.git_write import commit_files as github_commit_files



@tool(name="get_user", description=str(ToolDescriptionPrompt("git-get-user-tool-description")), approval_mode="never_require")
def get_user():
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
def commit_files(
    repo: Annotated[str, Field(description = _git_commit_fields.get("repo"))],
    file_path: Annotated[str, Field(description = _git_commit_fields.get("file_path"))],
    commit_message: Annotated[str, Field(description = _git_commit_fields.get("commit_message"))],
    branch: Annotated[str, Field(description = _git_commit_fields.get("branch"))],
    content: Annotated[str, Field(description = _git_commit_fields.get("content"))]
):

    return github_commit_files(
        repo=repo,
        file_path=file_path,
        commit_message=commit_message,
        branch=branch,
        content=content
    )


if __name__ == "__main__":
    commit_files(repo="Hari-var/test_repo", file_path="docs/README.md", commit_message="Add README with dummy content", branch="feature/add-readme", content="# Demo README\n\nThis is a sample README file created by an automated MAF agent.\n\n## Purpose\nThis repository is used for testing automated GitHub operations.\n\n## Notes\n- This is dummy content\n- Created for testing purposes")
