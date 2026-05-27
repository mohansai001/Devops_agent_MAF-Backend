# from utils.config import hari_github_token as github_token
from utils.config import hari_github_token as github_token
from github import Github, Auth #type: ignore
from utils.request_context import github_pat_ctx


def get_github_client(git_token=None):
    git_token = git_token or github_pat_ctx.get(None) or github_token
    auth = Auth.Token(git_token)
    return Github(auth=auth)