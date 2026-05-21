import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from utils.github_client import get_github_client 
from utils.logger import get_logger
from utils.config import github_token,REPO_OWNER

logger = get_logger(__name__)


def github_find_folder(cloud, resource_type, repo_owner=REPO_OWNER, repo_name="Terraform_modules", g=get_github_client()):
    logger.info(f"[github_agent] [github_find_folder] Searching for modules/{cloud}/{resource_type}")
    try:
        
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        tree = repo.get_git_tree("HEAD", recursive=True).tree
        # print(tree)
        target_path = f"modules/{cloud}/{resource_type}"
        found_paths = []
        for item in tree:
            if item.path.startswith(target_path):
                if item.type == 'blob':
                    found_paths.append(item.path)
        logger.info(f"[github_agent] [github_find_folder] Total module files found for {cloud}/{resource_type}: {len(found_paths)}")
        print(f"Total module files found for {cloud}/{resource_type}: {len(found_paths)}")
        print("Found files:", found_paths)
        print("=" * 30)
        return found_paths
    except Exception as e:
        logger.error(f"[github_agent] [github_find_folder] Error searching GitHub repo: {e}", exc_info=True)
        print(f"Error searching GitHub repo: {e}")
        return []
    
if __name__ == "__main__":
    print(github_find_folder("azure", "webapp"))