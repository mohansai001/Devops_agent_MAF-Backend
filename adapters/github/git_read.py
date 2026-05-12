
from utils.logger import get_logger
from utils.github_client import get_github_client

logger=get_logger(__name__)
REPO_OWNER = "Hari-var"
g = get_github_client()

def github_read_contents(path, repo_owner=REPO_OWNER, repo_name="Terraform_modules"):
    logger.info(f"[github_read_contents] Reading content from path: {path}")
    try:
        
        print(f"Reading content from path: {path}")
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        content = repo.get_contents(path)
        decoded_content = content.decoded_content.decode()
        logger.info(f"[github_read_contents] Successfully read content from {path}")
        print(f"Successfully read content from {path}")
        return decoded_content
    except Exception as e:
        logger.error(f"[github_read_contents] Error reading GitHub file content from {path}: {e}", exc_info=True)
        print(f"Error reading GitHub file content from {path}: {e}")
        return None