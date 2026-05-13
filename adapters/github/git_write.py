from utils.logger import get_logger
from utils.github_client import get_github_client
from github import GithubException # type: ignore

g = get_github_client()

def commit_files(
    repo: str,
    file_path: str,
    commit_message: str,
    branch: str,
    content: str
):
    print(f"Committing changes to {repo}/{file_path} on branch '{branch}'")

    # --- Input validation ---
    if not repo or "/" not in repo:
        return "Invalid repo format. Use 'owner/repo'."
    if not file_path or file_path.startswith(".git/"):
        return "Invalid file path. Must be relative to repo root and not a .git path."
    if not commit_message.strip():
        return "Commit message cannot be empty."
    if not branch.strip():
        return "Branch name cannot be empty."
    if not content.strip():
        return "File content cannot be empty."

    try:
        # --- Validate repo exists and is accessible ---
        try:
            repository = g.get_repo(repo)
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
    