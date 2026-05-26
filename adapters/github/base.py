from github import Github #type: ignore
from typing import Optional, List, Dict, Any
from utils.github_client import get_github_client

class GitHubAPIWrapper:
    def __init__(self, g: Github = None):
        self.g = g if g else get_github_client()


    def get_repo(self, full_name: str):
        return self.g.get_repo(full_name)

    def create_file(self, repo_full_name, path, message, content, branch="main"):
        repo = self.get_repo(repo_full_name)
        return repo.create_file(path, message, content, branch=branch)

    def update_file(self, repo_full_name, path, message, content, sha, branch="main"):
        repo = self.get_repo(repo_full_name)
        return repo.update_file(path, message, content, sha, branch=branch)

    def delete_file(self, repo_full_name, path, message, sha, branch="main"):
        repo = self.get_repo(repo_full_name)
        return repo.delete_file(path, message, sha, branch=branch)

    def get_contents(self, repo_full_name, path, ref=None):
        repo = self.get_repo(repo_full_name)
        return repo.get_contents(path, ref=ref)

    def get_commits(self, repo_full_name, sha=None, path=None, since=None, until=None, author=None):
        repo = self.get_repo(repo_full_name)
        return repo.get_commits(sha=sha, path=path, since=since, until=until, author=author)

    def get_commit(self, repo_full_name, sha):
        repo = self.get_repo(repo_full_name)
        return repo.get_commit(sha)

    def edit_repo(self, repo_full_name, **kwargs):
        repo = self.get_repo(repo_full_name)
        return repo.edit(**kwargs)

    def get_branches(self, repo_full_name):
        repo = self.get_repo(repo_full_name)
        return repo.get_branches()

    def get_branch(self, repo_full_name, name):
        repo = self.get_repo(repo_full_name)
        return repo.get_branch(name)

    def rename_branch(self, repo_full_name, branch, new_name):
        repo = self.get_repo(repo_full_name)
        return repo.rename_branch(branch, new_name)

    def create_git_ref(self, repo_full_name, ref, sha):
        repo = self.get_repo(repo_full_name)
        return repo.create_git_ref(ref, sha)

    def get_collaborators(self, repo_full_name):
        repo = self.get_repo(repo_full_name)
        return repo.get_collaborators()

    def get_topics(self, repo_full_name):
        repo = self.get_repo(repo_full_name)
        return repo.get_topics()

    def replace_topics(self, repo_full_name, topics: List[str]):
        repo = self.get_repo(repo_full_name)
        return repo.replace_topics(topics)

    def get_deployments(self, repo_full_name):
        repo = self.get_repo(repo_full_name)
        return repo.get_deployments()

    def create_deployment(self, repo_full_name, **kwargs):
        repo = self.get_repo(repo_full_name)
        return repo.create_deployment(**kwargs)

    def get_stats_contributors(self, repo_full_name):
        repo = self.get_repo(repo_full_name)
        return repo.get_stats_contributors()

    def get_stats_commit_activity(self, repo_full_name):
        repo = self.get_repo(repo_full_name)
        return repo.get_stats_commit_activity()

    def get_stats_participation(self, repo_full_name):
        repo = self.get_repo(repo_full_name)
        return repo.get_stats_participation()

    def get_views_traffic(self, repo_full_name):
        repo = self.get_repo(repo_full_name)
        return repo.get_views_traffic()

    def get_clones_traffic(self, repo_full_name):
        repo = self.get_repo(repo_full_name)
        return repo.get_clones_traffic()

    def merge_upstream(self, repo_full_name):
        repo = self.get_repo(repo_full_name)
        return repo.merge_upstream()

    def transfer(self, repo_full_name, new_owner):
        repo = self.get_repo(repo_full_name)
        return repo.transfer(new_owner)

    # 🔀 Pull Requests
    def create_pull(self, repo_full_name, title, body, base, head, draft=False):
        repo = self.get_repo(repo_full_name)
        return repo.create_pull(title=title, body=body, base=base, head=head, draft=draft)

    # ... Add all other PR methods similarly ...

    # 🐛 Issues
    def create_issue(self, repo_full_name, title, body=None, assignee=None, labels=None, milestone=None):
        repo = self.get_repo(repo_full_name)
        
        # PyGitHub silently ignores None for labels — pass empty list explicitly
        kwargs = {
            "title": title
        }

        if body is not None:
            kwargs["body"] = body

        if assignee is not None:
            kwargs["assignee"] = assignee

        if labels is not None:
            kwargs["labels"] = labels

        if milestone is not None:
            kwargs["milestone"] = milestone

        issue = repo.create_issue(**kwargs)

        return issue
        
        print(f"[create_issue] Created issue #{issue.number}: {issue.html_url}")
        return issue
    # ... Add all other Issue methods similarly ...

    # 🌿 Branches & Git Objects
    def get_git_ref(self, repo_full_name, ref):
        repo = self.get_repo(repo_full_name)
        return repo.get_git_ref(ref)

    # ... Add all other Git Object methods similarly ...

    # ✅ Checks & CI Status
    def create_check_run(self, repo_full_name, name, head_sha, status=None, conclusion=None):
        repo = self.get_repo(repo_full_name)
        return repo.create_check_run(name=name, head_sha=head_sha, status=status, conclusion=conclusion)

    # ... Add all other Checks methods similarly ...

    # 📦 Releases
    def create_git_release(self, repo_full_name, tag, name, message, draft=False, prerelease=False):
        repo = self.get_repo(repo_full_name)
        return repo.create_git_release(tag=tag, name=name, message=message, draft=draft, prerelease=prerelease)

    # ... Add all other Release methods similarly ...

    # 👤 Users & Organizations
    def get_user(self, username=None):
        return self.g.get_user(username) if username else self.g.get_user()

    def get_organization(self, org):
        return self.g.get_organization(org)

    # ... Add all other User/Org methods similarly ...

    # ⚙️ Workflows (GitHub Actions)
    def get_workflows(self, repo_full_name):
        repo = self.get_repo(repo_full_name)
        return repo.get_workflows()

    # ... Add all other Workflow methods similarly ...

    # 🔔 Webhooks
    def create_hook(self, repo_full_name, name, config, events, active=True):
        repo = self.get_repo(repo_full_name)
        return repo.create_hook(name, config, events, active)

    # ... Add all other Webhook methods similarly ...

    # 🔍 Search
    def search_repositories(self, query):
        return self.g.search_repositories(query)

    def search_issues(self, query):
        return self.g.search_issues(query)

    def search_commits(self, query):
        return self.g.search_commits(query)

    def search_code(self, query):
        return self.g.search_code(query)

    def search_users(self, query):
        return self.g.search_users(query)

    # 📊 Rate Limiting & Auth
    def get_rate_limit(self):
        return self.g.get_rate_limit()

    @property
    def rate_limiting(self):
        return self.g.rate_limiting

    @property
    def rate_limiting_resettime(self):
        return self.g.rate_limiting_resettime
 