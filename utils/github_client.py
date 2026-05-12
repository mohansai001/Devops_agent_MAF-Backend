from utils.config import github_token
from github import Github, Auth #type: ignore


def get_github_client():
    auth = Auth.Token(github_token)
    return Github(auth=auth)