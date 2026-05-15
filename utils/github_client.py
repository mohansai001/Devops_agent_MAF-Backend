# from utils.config import hari_github_token as github_token
from utils.config import github_token
from github import Github, Auth #type: ignore


def get_github_client(git_token=github_token):
    auth = Auth.Token(git_token)
    return Github(auth=auth)