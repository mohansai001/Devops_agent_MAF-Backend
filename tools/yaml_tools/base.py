from agent_framework import tool #type: ignore
from typing import Annotated
from pydantic import Field
from agent_framework import tool #type: ignore
from typing import Annotated
from pydantic import Field
import requests
import yaml
import base64
from github import Github, Auth
from openai import OpenAI
import asyncio
import os
from utils.config import AZURE_AI_API_KEY,github_token
from openai import AzureOpenAI
auth = Auth.Token(github_token)
g = Github(auth=auth)
REPO_OWNER = "RAGHAVENDRA-VAM"
from utils.clientConnection import get_client
from utils.config import Base_agent_config,Content_generator_model_config
from content_generator import create_yaml_scripts, clean_yaml_output

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
        except:
            # File doesn't exist, create it
            repo.create_file(
                path=file_path,
                message=commit_message,
                content=file_content,
                branch=branch
            )
            print(f"Created {file_path}")



@tool(name="CI_builder", description="Builds a CI pipeline based on the given requirements", approval_mode="never_require")
async def CI_Builder(tool: Annotated[str, Field(description="The CI tool to used for the application the tool name should be in lower case without spaces, the sapce should be replaces with '_' .Example : github_actions")],
                     techstack: Annotated[str, Field(description="The tech stack that is used to develop the application and in the repository, The tech stack name should be in lower case. Example : python")],
                     repo_name: Annotated[str, Field(description="The repository name")]):
   #Assuming Tech stack,tool, Repository name and Framework comes from the orchestrator agent
   try:
    print("called CI Builder.........\n")
    print("Tech Stack:", techstack,"\n====================")
    yaml_data=github_read_yaml_library()
    paths = get_cicd_paths(yaml_data, tool, techstack)
    ci_template=github_read_yaml_library(paths["ci"])
    instructions=f"""You are a Senior DevOps Engineer. 
    Your job is to take a CI/CD pipeline YAML template and generate a complete, fully working pipeline script.
    - Replace placeholders with real, working values
    - Use '{repo_name}' as the repository name wherever needed
    - Output ONLY valid YAML, no explanations or markdown.Below is the attached ci template {ci_template}"""
    ci_script=create_yaml_scripts(instructions)
    
    ci_repo_name="Workflow-files"
    github_push_files(
            {f".github/workflows/{techstack}-ci.yml": ci_script},
            ci_repo_name,
            "Add CI pipeline",
            "main"
        )
   except Exception as e:
       print("Error occurred while creating CI pipeline:", e)


@tool(name="CD_builder", description="Builds a CD pipeline based on the given requirements", approval_mode="never_require")
async def CD_Builder(target: Annotated[str, Field(description="The target environment for the CD pipeline")],
                     techstack: Annotated[str, Field(description="The tech stack that is used to develop the application and in the repo")],
                     repo_name: Annotated[str, Field(description="The repository name")],
                     tool: Annotated[str, Field(description="The CI tool to use")]):
   #Assuming Tech stack,tool, Repository name and Framework comes from the orchestrator agent
   yaml_data=github_read_yaml_library()
   paths = get_cicd_paths(yaml_data, tool, target=target)
   cd_template=github_read_yaml_library(paths["cd"])
   instructions=f"""You are a Senior DevOps Engineer. 
    Your job is to take a CI/CD pipeline YAML template and generate a complete, fully working pipeline script.
    - Replace placeholders with real, working values
    - Use '{repo_name}' as the repository name wherever needed
    - Output ONLY valid YAML, no explanations or markdown.Below is the attached cd template {cd_template}"""
   cd_script=create_yaml_scripts(instructions)
   
   github_push_files(
        {f".github/workflows/{target}-cd.yml": cd_script},
        repo_name,
        "Add CD pipeline",
        "main"
    )
   

@tool(name="TF_Builder", description="Builds a Terraform yaml based on the given requirements", approval_mode="never_require")
async def TF_Builder(cloud_provider: Annotated[str, Field(description="The cloud provider to be used for the infrastructure (e.g., 'azure', 'aws', 'gcp')")],
                     resource_group: Annotated[str, Field(description="The resource group to be used for the infrastructure")],
                     resources: Annotated[str, Field(description="The resources to be provisioned in the infrastructure")],
                     repo_name: Annotated[str, Field(description="The repository name")]):
    print("Called TF_Builder tool...")
    prompt = f"You are a senior Devops Platform Engineer. Generate a production grade Terraform pipeline yml for {cloud_provider} with the following details:\n\n"
    prompt += f"Resource Group: {resource_group}\n"
    prompt += f"Resources: {resources}\n"
    prompt += f"Repository: {repo_name}\n"
    print("Prompt for Terraform YAML generation:\n", prompt,"\n================")
    tf_script = await create_yaml_scripts(prompt)
    
    tf_repo_name="Workflow-files"
    print("Response..............:\n",tf_script)
    github_push_files(
        {f".github/workflows/{repo_name}-tf.yml": tf_script},
        tf_repo_name,
        "Added CD pipeline",
        "main"
    )
    print("==================TASK Completed===================")
    return f"TASK COMPLETED: {tf_script}"
