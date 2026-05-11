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
from utils.clientConnection import client
import asyncio
import os
from utils.config import AZURE_AI_API_KEY,github_token
from openai import AzureOpenAI

auth = Auth.Token(github_token)
g = Github(auth=auth)
REPO_OWNER = "RAGHAVENDRA-VAM"





def get_tf_yaml_scripts(text):
    try:
        endpoint = "https://devops-maf1.openai.azure.com"
        deployment = "gpt-4.1-nano"
        subscription_key = AZURE_AI_API_KEY
        api_version = "2024-12-01-preview"
        # print("Azure configuration:\n", f"Endpoint: {endpoint}\nDeployment: {deployment}\nAPI Version: {api_version}")
        if not subscription_key:
            print("Error: AZURE_OPENAI_KEY not found in environment variables")
            return "Error: AZURE_OPENAI_KEY not found in environment variables"
 
        client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=subscription_key,
        )
        print("Azure client initialized successfully.\n",client)
 
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": text,
                }
            ],
            max_tokens=1000,
            temperature=0.7,
            model=deployment
        )
        print("Azure response for Terraform yml script:\n",response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        AI_ERROR_COUNT.labels(model='azure', error_type=type(e).__name__).inc()
        print(f"Azure Error: {str(e)}")
        return f"Azure Error: {str(e)}"
 


def get_azure_response(yaml_template,repo_name):
    print("Inside get_azure_response")
    instructions=f"""You are a Senior DevOps Engineer. 
Your job is to take a CI/CD pipeline YAML template {yaml_template} and generate a complete, fully working pipeline script.
- Replace placeholders with real, working values
- Use '{repo_name}' as the repository name wherever needed
- Output ONLY valid YAML, no explanations or markdown"""
    try:
        endpoint = "https://defaultresourcegroup-ccan-resource-0475.cognitiveservices.azure.com/"
        deployment = "gpt-4.1-mini-312634"
        subscription_key = AZURE_AI_API_KEY
        api_version = "2024-12-01-preview"
        print("Azure configuration:\n", f"Endpoint: {endpoint}\nDeployment: {deployment}\nAPI Version: {api_version}")
        if not subscription_key:
            return "Error: AZURE_OPENAI_KEY not found in environment variables"
 
        client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=subscription_key,
        )
        print("Azure client initialized successfully.\n",client)
 
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": instructions,
                }
            ],
            max_tokens=1000,
            temperature=0.7,
            model=deployment
        )
        print("Azure response:\n", response)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Azure Error: {str(e)}")
        return f"Azure Error: {str(e)}"
 



def create_yaml_scripts(yaml_template,repo_name):
    agent = client.as_agent(
    name="HelloAgent",
#     instructions=f"You are Senior Devops Engineer who writes CI/CD pipelines. Below is the template for creating a CI Pipeline follow the template and generate the working script using the template in the yaml format.Below is the repo name {repo_name}. Fill out the details wherever needed",
# )
    instructions=f"""You are a Senior DevOps Engineer. 
Your job is to take a CI/CD pipeline YAML template and generate a complete, fully working pipeline script.
- Replace placeholders with real, working values
- Use '{repo_name}' as the repository name wherever needed
- Output ONLY valid YAML, no explanations or markdown""",
    )
    template_str = yaml.dump(yaml_template, default_flow_style=False) if isinstance(yaml_template, dict) else yaml_template
    result = asyncio.run(agent.run(template_str))

    # result = asyncio.run(agent.run(yaml_template))
    # print("agent:\n", result)
    # Try .text or .content
    clean_yaml = "\n".join([line for line in result.text.splitlines() if not line.strip().startswith("```")])

    print(clean_yaml)
    return clean_yaml


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
async def CI_Builder(tool: Annotated[str, Field(description="The CI tool to used for the application")],
                     techstack: Annotated[str, Field(description="The tech stack that is used to develop the application and in the repo")],
                     repo_name: Annotated[str, Field(description="The repository name")]):
   #Assuming Tech stack,tool, Repository name and Framework comes from the orchestrator agent
   yaml_data=github_read_yaml_library()
   paths = get_cicd_paths(yaml_data, tool, techstack)
   ci_template=github_read_yaml_library(paths["ci"])
   ci_script=create_yaml_scripts(ci_template, "Workflow-files")
   github_push_files(
        {f".github/workflows/{techstack}-ci.yml": ci_script},
        repo_name,
        "Add CI pipeline",
        "main"
    )



@tool(name="CD_builder", description="Builds a CD pipeline based on the given requirements", approval_mode="never_require")
async def CD_Builder(target: Annotated[str, Field(description="The target environment for the CD pipeline")],
                     techstack: Annotated[str, Field(description="The tech stack that is used to develop the application and in the repo")],
                     repo_name: Annotated[str, Field(description="The repository name")],
                     tool: Annotated[str, Field(description="The CI tool to use")]):
   #Assuming Tech stack,tool, Repository name and Framework comes from the orchestrator agent
   yaml_data=github_read_yaml_library()
   paths = get_cicd_paths(yaml_data, tool, target=target)
   cd_template=github_read_yaml_library(paths["cd"])
   cd_script=create_yaml_scripts(cd_template, "Workflow-files")
   github_push_files(
        {f".github/workflows/{target}-cd.yml": cd_script},
        repo_name,
        "Add CD pipeline",
        "main"
    )
   


@tool(name="CD_builder", description="Builds a CD pipeline based on the given requirements", approval_mode="never_require")
async def CD_Builder(target: Annotated[str, Field(description="The target environment for the CD pipeline")],
                     techstack: Annotated[str, Field(description="The tech stack that is used to develop the application and in the repo")],
                     repo_name: Annotated[str, Field(description="The repository name")],
                     tool: Annotated[str, Field(description="The CI tool to use")]):
   #Assuming Tech stack,tool, Repository name and Framework comes from the orchestrator agent
   yaml_data=github_read_yaml_library()
   paths = get_cicd_paths(yaml_data, tool, target=target)
   cd_template=github_read_yaml_library(paths["cd"])
   cd_script=create_yaml_scripts(cd_template, "Workflow-files")
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
   # Assuming Cloud provider, Resource group, Resources and Repository name comes from the orchestrator agent
    print("Called TF_Builder agent...")
    prompt = f"You are a senior Devops Platform Engineer. Generate a production grade Terraform configuration yml for {cloud_provider} with the following details:\n\n"
    prompt += f"Resource Group: {resource_group}\n"
    prompt += f"Resources: {resources}\n"
    prompt += f"Repository: {repo_name}\n"

    response = await get_tf_yaml_scripts(prompt)
    print("Response:\n",response)
    return f"TASK COMPLETED: {response}"
