import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import time
from github.GithubException import GithubException #type: ignore

from utils.logger import get_logger
from utils.github_client import get_github_client
from utils.config import hari_github_token as GITHUB_TOKEN,REPO_OWNER
from github import Github #type: ignore

logger=get_logger(__name__)
g = get_github_client()

def github_read_contents(path, repo_owner=REPO_OWNER, repo_name="Terraform_modules"):
    logger.info(f"[github_agent] [github_read_contents] Reading content from path: {path}")
    try:
        
        print(f"Reading content from path: {path}")
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        content = repo.get_contents(path)
        decoded_content = content.decoded_content.decode()
        logger.info(f"[github_agent] [github_read_contents] Successfully read content from {path}")
        print(f"Successfully read content from {path}")
        return decoded_content
    except Exception as e:
        logger.error(f"[github_agent] [github_read_contents] Error reading GitHub file content from {path}: {e}", exc_info=True)
        print(f"Error reading GitHub file content from {path}: {e}")
        return None
    
def wait_for_latest_workflow(
        repo_name: str,
        workflow_file_name: str = "ci.yml",
        branch: str = "main",
        poll_interval: int = 10,
        timeout: int = 800,
        g: Github = g
    ):
        logger.info(f"[github_agent] [wait_for_latest_workflow] Monitoring workflow in repo: {repo_name}")
        print(f"Repo Name: {repo_name},\n Workflow File: {workflow_file_name},\n Branch: {branch}")
        """
        Waits for latest workflow execution to complete.
 
        Returns:
            True  -> workflow succeeded
            False -> workflow failed/cancelled/timed out
        """
        repo = g.get_repo(repo_name)
        start_time = time.time()
 
        print(f"Monitoring workflow: {workflow_file_name}")
        # print(f"Repository: {repo.full_name}")
 
        try:
            workflow = repo.get_workflow(workflow_file_name)
            print(f"Workflow ID   : {workflow.id}")
            print(f"Workflow Name : {workflow.name}")
            print(f"State         : {workflow.state}")
            print(f"Path          : {workflow.path}")
            print(f"URL           : {workflow.html_url}")
            
        except GithubException as e:
            logger.warning(f"[github_agent] [wait_for_latest_workflow] Unable to find workflow '{workflow_file_name}'")
            print(f"Unable to find workflow '{workflow_file_name}'")
            print(str(e))
            return False
 
 
        while True:
 
            # Timeout check
            if time.time() - start_time > timeout:
                logger.warning(f"[github_agent] [wait_for_latest_workflow] Timeout reached while waiting for workflow: {workflow_file_name}")
                print("Workflow monitoring timed out")
                return False
 
            try:
                runs = workflow.get_runs(branch=branch)

                # Debug print
                print(f"Total runs: {runs.totalCount}")
                for i, run in enumerate(runs[:5]):  # print first 5 runs
                    print(f"  [{i}] id={run.id} status={run.status} conclusion={run.conclusion} created_at={run.created_at}")
 
                if runs.totalCount == 0:
                    logger.info(f"[wait_for_latest_workflow]")
                    print("Waiting for workflow run to start...")
                    time.sleep(poll_interval)
                    continue
 
                latest_run = runs[0]
 
                # # Store first detected run id
                # if latest_run_id is None:
                #     latest_run_id = latest_run.id
                #     print(f"Detected workflow run: {latest_run_id}")
 
                # # Prevent older workflow confusion
                # if latest_run.id != latest_run_id:
                #     latest_run = repo.get_workflow_run(latest_run_id)
 
                print("=" * 60)
                print(f"Workflow Name : {latest_run.name}")
                print(f"Run ID        : {latest_run.id}")
                print(f"Branch        : {latest_run.head_branch}")
                print(f"Status        : {latest_run.status}")
                print(f"Conclusion    : {latest_run.conclusion}")
                print(f"URL           : {latest_run.html_url}")
                print("=" * 60)
 
                # Still running
                if latest_run.status != "completed":
                    time.sleep(poll_interval)
                    continue
 
                # SUCCESS
                if latest_run.conclusion == "success":
                    print("Workflow completed successfully")
                    return True
 
                # FAILURE
                print(f"Workflow failed with status: {latest_run.conclusion}")
                return False
 
            except Exception as e:
                print(f"Monitoring error: {str(e)}")
                time.sleep(poll_interval)

def get_artifact_name_from_run(repo_name: str, workflow_file_name: str, branch: str = "main"):
    """
    Fetches the artifact name directly from the GitHub Artifacts API
    for the latest completed workflow run.
    """
    repo = g.get_repo(repo_name)
    
    try:
        workflow = repo.get_workflow(workflow_file_name)
        runs = workflow.get_runs(branch=branch, status="completed")
        
        if runs.totalCount == 0:
            print("No completed runs found.")
            return None, None
        
        latest_run = runs[0]
        print(f"Checking artifacts for Run ID: {latest_run.id}")
        
        # List all artifacts for this run
        artifacts = repo.get_artifacts()  # or use the run-specific endpoint below
        
        # Use raw requester for run-scoped artifacts
        _, response = repo._requester.requestJsonAndCheck(
            "GET",
            f"/repos/{repo_name}/actions/runs/{latest_run.id}/artifacts"
        )
        
        artifact_names = [artifact["name"] for artifact in response.get("artifacts", [])]
        workflow_name = latest_run.name
        print(f"Found artifacts: {artifact_names}")
        
        # Return the first match or filter by pattern
        for name in artifact_names:
            if "drop" in name:  # adjust filter to your naming convention
                return name, workflow_name
        if artifact_names:

            return artifact_names[0], workflow_name
        else:
            return None, None
    
    except Exception as e:
        print(f"Error fetching artifacts: {e}")
        return None, None
    

import zipfile
import io
import re    

def get_deployment_url_from_logs(repo_name: str, workflow_file_name: str, branch: str = "main") -> str | None:
    repo = g.get_repo(repo_name)
    
    try:
        workflow = repo.get_workflow(workflow_file_name)
        runs = workflow.get_runs(branch=branch, status="completed")
        
        if runs.totalCount == 0:
            print("No completed runs found.")
            return None
        
        latest_run = runs[0]
        
        # Download logs zip
        _, raw_zip = repo._requester.requestBlobAndCheck(
            "GET",
            f"/repos/{repo_name}/actions/runs/{latest_run.id}/logs"
        )
        
        with zipfile.ZipFile(io.BytesIO(raw_zip)) as zf:
            for file_name in zf.namelist():
                # Target deploy job log file
                if "deploy" in file_name.lower():
                    with zf.open(file_name) as log_file:
                        log_content = log_file.read().decode("utf-8", errors="replace")
                        
                        # Match any HTTP/HTTPS URL in the logs
                        match = re.search(
                            r'https?://[^\s\'"<>\]]+',
                            log_content
                        )
                        if match:
                            return match.group(0)
        
        print("Deployment URL not found in logs.")
        return None
    
    except Exception as e:
        print(f"Error retrieving deployment URL: {e}")
        return None
import requests  
def get_cd_run_metadata(repo_name: str, workflow_file_name: str, branch: str = "main") -> dict | None:
    repo = g.get_repo(repo_name)

    try:
        workflow = repo.get_workflow(workflow_file_name)
        runs = workflow.get_runs(branch=branch, status="completed")

        if runs.totalCount == 0:
            print("No completed runs found.")
            return None

        latest_run = runs[0]

        # ── Fetch logs via requests (handles redirect) ────────────────────
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }
        response = requests.get(latest_run.logs_url, headers=headers, allow_redirects=True)
        response.raise_for_status()

        deployment_url = None

        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
            print("Log files:", zf.namelist())

            for file_name in zf.namelist():
                if "deploy" in file_name.lower():
                    with zf.open(file_name) as log_file:
                        log_content = log_file.read().decode("utf-8", errors="replace")

                        # Primary: Azure App Service URL line
                        match = re.search(
                            r'App Service Application URL:\s*(https?://[^\s\'"<>\]]+)',
                            log_content,
                            re.IGNORECASE
                        )
                        if match:
                            deployment_url = match.group(1)
                            break

        return {
            "workflow_name" : latest_run.name,
            "run_id"        : latest_run.id,
            "branch"        : latest_run.head_branch,
            "conclusion"    : latest_run.conclusion,
            "deployment_url": deployment_url   # ✅ https://testingwebapp-xxx.azurewebsites.net
        }

    except zipfile.BadZipFile:
        print("Not a valid zip — check token or redirect.")
        return None
    except Exception as e:
        print(f"Error fetching CD metadata: {e}")
        return None

if __name__ == "__main__":
    repo_name = "Hari-var/insure-flow-webapp"
    file_name = "webapp-cd.yml"
    branch = "master"
    result = get_cd_run_metadata(repo_name=repo_name, workflow_file_name=file_name, branch=branch)
    print(result)