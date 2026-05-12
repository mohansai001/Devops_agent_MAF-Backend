from agent_framework import tool #type: ignore
from typing import Annotated
from pydantic import Field
from agent_framework import tool #type: ignore
from typing import Annotated
from pydantic import Field
import requests
import yaml
import base64
from github import Github, Auth #type: ignore
from openai import OpenAI, AzureOpenAI  #type: ignore
import asyncio
import os
from utils.config import AZURE_AI_API_KEY,github_token

auth = Auth.Token(github_token)
g = Github(auth=auth)
REPO_OWNER = "RAGHAVENDRA-VAM"
from utils.clientConnection import get_client
from .content_generator import create_yaml_scripts
from utils.logger import get_logger
logger = get_logger(__name__)

# client = get_client(model=Content_generator_model_config.model, endpoint=Content_generator_model_config.AI_content_endpoint,api_version = "2024-05-01-preview")

def github_read_yaml_library(FILE_PATH="file-paths-registry.yml"):
    REPO_OWNER = "RAGHAVENDRA-VAM"
    REPO_NAME = "Yaml-Templates"
    repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
    file = repo.get_contents(f"{FILE_PATH}")
    return yaml.safe_load(file.decoded_content.decode())

def get_cicd_paths(config, tool, language=None, target=None):
    result = {}

    tool_data = config.get("cicd_tools", {}).get(tool, {})

    if not tool_data:
        raise ValueError(f"Invalid tool: {tool}")

    # Extract CI template
    if language:
        ci_templates = tool_data.get("ci_templates", {})
        ci_path = ci_templates.get(language)

        if not ci_path:
            raise ValueError(f"CI template not found for language: {language}")

        result["ci"] = ci_path

    # Extract CD template
    if target:
        cd_templates = tool_data.get("cd_templates", {})
        cd_path = cd_templates.get(target)

        if not cd_path:
            raise ValueError(f"CD template not found for target: {target}")

        result["cd"] = cd_path

    return result

def github_push_files(files_to_push, repo_name, commit_message, branch="main"):
    repo = g.get_repo(f"{REPO_OWNER}/{repo_name}")
    print("In the github_push_files function\n")
    results = []
    for file_path, file_content in files_to_push.items():
        try:
            # Try to get existing file
            existing_file = repo.get_contents(file_path, ref=branch)
            # Update existing file
            repo.update_file(
                path=file_path,
                message=commit_message,
                content=file_content,
                sha=existing_file.sha,
                branch=branch
            )
            print(f"Updated {file_path}")
            results.append({"file": file_path, "action": "updated"})
        except Exception as e:
            try:
                # File doesn't exist, create it
                repo.create_file(
                    path=file_path,
                    message=commit_message,
                    content=file_content,
                    branch=branch
                )
                print(f"Created {file_path}")
                results.append({"file": file_path, "action": "created"})
            except Exception as ce:
                print(f"Failed to create {file_path}: {ce}")
                results.append({"file": file_path, "action": "error", "error": str(ce)})
    return results



@tool(name="CI_builder", description="Builds a CI pipeline based on the given requirements", approval_mode="never_require")
async def CI_Builder(tool: Annotated[str, Field(description="The CI tool to used for the application the tool name should be in lower case without spaces, the sapce should be replaces with '_' .Example : github_actions")],
                     techstack: Annotated[str, Field(description="The tech stack that is used to develop the application and in the repository, The tech stack name should be in lower case. Example : python")],
                     repo_name: Annotated[str, Field(description="The repository name")]):
    # Assuming Tech stack, tool, Repository name and Framework comes from the orchestrator agent
    try:
        logger.info("[CI_Builder] Tool called.")
        print("[CI_Builder] Tool called.")
        logger.info(f"[CI_Builder] Input parameters - Tech Stack: {techstack}, Tool: {tool}, Repo Name: {repo_name}")
        print(f"[CI_Builder] Input parameters - Tech Stack: {techstack}, Tool: {tool}, Repo Name: {repo_name}")
        print(f"Tech Stack: {techstack}")

        logger.info("[CI_Builder] Reading YAML library for CI template paths...")
        print("[CI_Builder] Reading YAML library for CI template paths...")
        yaml_data = github_read_yaml_library()
        logger.info(f"[CI_Builder] YAML data keys: {list(yaml_data.keys())}")
        print(f"[CI_Builder] YAML data keys: {list(yaml_data.keys())}")

        paths = get_cicd_paths(yaml_data, tool, techstack)
        logger.info(f"[CI_Builder] CI template path: {paths.get('ci')}")
        print(f"[CI_Builder] CI template path: {paths.get('ci')}")

        ci_template = github_read_yaml_library(paths["ci"])
        logger.info("[CI_Builder] Loaded CI template from YAML library.")
        print("[CI_Builder] Loaded CI template from YAML library.")

        logger.info("[CI_Builder] Preparing instructions for CI pipeline generation.")
        print("[CI_Builder] Preparing instructions for CI pipeline generation.")
        instructions = f"""You are a Senior DevOps Engineer. 
Your job is to take a CI/CD pipeline YAML template and generate a complete, fully working pipeline script.
- Replace placeholders with real, working values
- Use '{repo_name}' as the repository name wherever needed
- Output ONLY valid YAML, no explanations or markdown. Below is the attached ci template {ci_template}"""
        print("Instructions for CI pipeline generation:\n", instructions)

        logger.info("[CI_Builder] Generating CI pipeline script using content generator...")
        print("[CI_Builder] Generating CI pipeline script using content generator...")
        ci_script = create_yaml_scripts(instructions)

        ci_repo_name = "Workflow-files"  # Make ci_repo_name dynamic while deploying.....
        logger.info(f"[CI_Builder] Pushing CI Pipeline script into the repository: {ci_repo_name}")
        print(f"[CI_Builder] Pushing CI Pipeline script into the repository: {ci_repo_name}")
        result = github_push_files(
            {f".github/workflows/{techstack}-ci.yml": ci_script},
            ci_repo_name,
            "Add CI pipeline",
            "main"
        )
        logger.info(f"[CI_Builder] CI push result: {result}")
        print(f"[CI_Builder] CI push result: {result}")
    except Exception as e:
        logger.error(f"[CI_Builder] Error occurred while creating CI pipeline: {e}", exc_info=True)
        print(f"[CI_Builder] Error occurred while creating CI pipeline: {e}")


@tool(name="CD_builder", description="Builds a CD pipeline based on the given requirements", approval_mode="never_require")
async def CD_Builder(target: Annotated[str, Field(description="The target environment for the CD pipeline")],
                     techstack: Annotated[str, Field(description="The tech stack that is used to develop the application and in the repo")],
                     repo_name: Annotated[str, Field(description="The repository name")],
                     tool: Annotated[str, Field(description="The CI tool to use")]):
    # Assuming Tech stack, tool, Repository name and Framework comes from the orchestrator agent
    try:
        logger.info("[CD_Builder] Tool called.")
        print("[CD_Builder] Tool called.")
        logger.info(f"[CD_Builder] Input parameters - Tech Stack: {techstack}, Tool: {tool}, Repo Name: {repo_name}, Target: {target}")
        print(f"[CD_Builder] Input parameters - Tech Stack: {techstack}, Tool: {tool}, Repo Name: {repo_name}, Target: {target}")

        logger.info("[CD_Builder] Reading YAML library for CD template paths...")
        print("[CD_Builder] Reading YAML library for CD template paths...")
        yaml_data = github_read_yaml_library()
        # logger.info(f"[CD_Builder] YAML data keys: {list(yaml_data.keys())}")

        paths = get_cicd_paths(yaml_data, tool, target=target)
        logger.info(f"[CD_Builder] CD template path: {paths.get('cd')}")
        print(f"[CD_Builder] CD template path: {paths.get('cd')}")

        cd_template = github_read_yaml_library(paths["cd"])
        logger.info("[CD_Builder] Loaded CD template from YAML library.")
        print("[CD_Builder] Loaded CD template from YAML library.")

        logger.info("[CD_Builder] Preparing instructions for CD pipeline generation.")
        print("[CD_Builder] Preparing instructions for CD pipeline generation.")
        instructions = f"""You are a Senior DevOps Engineer. 
Your job is to take a CI/CD pipeline YAML template and generate a complete, fully working pipeline script.
- Replace placeholders with real, working values
- Use '{repo_name}' as the repository name wherever needed
- Output ONLY valid YAML, no explanations or markdown. Below is the attached cd template {cd_template}"""

        logger.info("[CD_Builder] Generating CD pipeline script using content generator...")
        print("[CD_Builder] Generating CD pipeline script using content generator...")
        cd_script = create_yaml_scripts(instructions)
        # Make the repo dynamic while deploying...
        cd_repo_name = "Workflow-files"
        logger.info(f"[CD_Builder] Pushing CD Pipeline script into the repository: {repo_name}")
        print(f"[CD_Builder] Pushing CD Pipeline script into the repository: {repo_name}")
        result = github_push_files(
            {f".github/workflows/{target}-cd.yml": cd_script},
            cd_repo_name,
            "Add CD pipeline",
            "main"
        )
        logger.info(f"[CD_Builder] CD push result: {result}")
        print(f"[CD_Builder] CD push result: {result}")
    except Exception as e:
        logger.error(f"[CD_Builder] Error occurred while creating CD pipeline: {e}", exc_info=True)
        print(f"[CD_Builder] Error occurred while creating CD pipeline: {e}")
   

@tool(name="TF_Builder", description="Builds a Terraform yaml based on the given requirements", approval_mode="never_require")
async def TF_Builder(cloud_provider: Annotated[str, Field(description="The cloud provider to be used for the infrastructure (e.g., 'azure', 'aws', 'gcp')")],
                     resource_group: Annotated[str, Field(description="The resource group to be used for the infrastructure")],
                     resources: Annotated[str, Field(description="The resources to be provisioned in the infrastructure")],
                     repo_name: Annotated[str, Field(description="The repository name")]):
    try:
        logger.info("[TF_Builder] Tool called.")
        print("[TF_Builder] Tool called.")
        logger.info(f"[TF_Builder] Input parameters - Cloud Provider: {cloud_provider}, Resource Group: {resource_group}, Resources: {resources}, Repo Name: {repo_name}")
        print(f"[TF_Builder] Input parameters - Cloud Provider: {cloud_provider}, Resource Group: {resource_group}, Resources: {resources}, Repo Name: {repo_name}")

        logger.info("[TF_Builder] Preparing prompt for Terraform YAML generation.")
        print("[TF_Builder] Preparing prompt for Terraform YAML generation.")
        prompt = f"You are a senior Devops Platform Engineer. Generate a production grade Terraform pipeline yml for {cloud_provider} with the following details:\n\n"
        prompt += f"Resource Group: {resource_group}\n"
        prompt += f"Resources: {resources}\n"
        prompt += f"Repository: {repo_name}\n"
        # logger.info(f"[TF_Builder] Prompt: {prompt}")
        print(f"[TF_Builder] Prompt: {prompt}")

        logger.info("[TF_Builder] Generating Terraform pipeline script using content generator...")
        print("[TF_Builder] Generating Terraform pipeline script using content generator...")
        tf_script = create_yaml_scripts(prompt)

        tf_repo_name = "Workflow-files"
        logger.info(f"[TF_Builder] Pushing Terraform Pipeline script into the repository: {tf_repo_name}")
        print(f"[TF_Builder] Pushing Terraform Pipeline script into the repository: {tf_repo_name}")
        result = github_push_files(
            {f".github/workflows/{repo_name}-tf.yml": tf_script},
            tf_repo_name,
            "Added CD pipeline",
            "main"
        )
        logger.info(f"[TF_Builder] TF push result: {result}")
        print(f"[TF_Builder] TF push result: {result}")
        logger.info("[TF_Builder] TASK COMPLETED")
        print("[TF_Builder] TASK COMPLETED")
        print("==================TASK Completed===================")
        return f"TASK COMPLETED: {tf_script}"
    except Exception as e:
        logger.error(f"[TF_Builder] Error occurred while creating Terraform pipeline: {e}", exc_info=True)
        print(f"[TF_Builder] Error occurred while creating Terraform pipeline: {e}")
