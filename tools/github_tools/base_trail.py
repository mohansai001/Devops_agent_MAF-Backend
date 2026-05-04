
from utils.config import github_token
from agent_framework import tool #type: ignore
from github import Github, Auth
from typing import Annotated
from pydantic import Field


def get_github_client():
    auth = Auth.Token(github_token)
    return Github(auth=auth)

@tool(name="get_user", description="Get the authenticated user information. ONLY use for debugging or authentication checks. DO NOT use for file or repo modifications.", approval_mode="never_require")
def get_user():
    print("github_token:", github_token)
    g_client = get_github_client()
    user = g_client.get_user()
    print("login:", user.login)
    print("type:", type(user))
    print(user)
    return user

@tool(name="commit_files",
        description="Create or update files in a GitHub repository. Use this when the task involves adding, modifying, or committing files.", 
        approval_mode="never_required")
def commit_changes(
    repo: Annotated[str, Field(description="Full repository name in 'owner/repo' format. Example: 'Hari-var/test_repo'. Never just 'repo'.")], 
    file_path: Annotated[str, Field(description="File path relative to repo root. Example: 'docs/README.md'. Never a .git path.")], 
    commit_message: Annotated[str, Field(description="The git commit message. Example: 'Add README with dummy content'")], 
    branch: Annotated[str, Field(description="Exact branch name to commit to. Example: 'feature/add-readme' or 'main'. Must be the target branch, not 'main' unless explicitly specified.")], 
    content: Annotated[str, Field(description="The full file content as a plain string. Must never be empty if adding or updating a file.")]
):
    print("Committing changes to the repository")
    print("repo:", repo)
    print("file_path:", file_path)
    print("commit_message:", commit_message)
    print("branch:", branch)
    print("content:", content)
    try:
        g_client = get_github_client()
        repository = g_client.get_repo(repo)
        repository.create_file(
            path=file_path,
            message=commit_message,
            content=content,
            branch=branch
        )
        return "Changes committed successfully"
    except Exception as e:
        print("Error committing changes:", e)
        return "Failed to commit changes"
    
    
if __name__ == "__main__":
    commit_changes(repo="Hari-var/test_repo", file_path="docs/README.md", commit_message="Add README with dummy content", branch="feature/add-readme", content="# Demo README\n\nThis is a sample README file created by an automated MAF agent.\n\n## Purpose\nThis repository is used for testing automated GitHub operations.\n\n## Notes\n- This is dummy content\n- Created for testing purposes")
