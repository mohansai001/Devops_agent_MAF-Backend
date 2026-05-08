from typing import Annotated
from pydantic import Field
from agent_framework import tool #type: ignore
import requests
import yaml
import base64
import asyncio
import os
import json
from utils.clientConnection import get_client
from utils.config import github_token,model_subscription_key
from github import Github, Auth
from ..yaml_tools.base import github_push_files
from openai import AzureOpenAI

GITHUB_TOKEN = github_token
client = get_client()
auth = Auth.Token(GITHUB_TOKEN)
g = Github(auth=auth)
REPO_OWNER = "RAGHAVENDRA-VAM"

def get_azure_response(content, file_name, cloud_provider, resource_group_dict, resource):
    print("Inside azure call.....")
    
    # Convert dictionaries to strings for the prompt if needed
    resource_str = json.dumps(resource, indent=2) if isinstance(resource, dict) else str(resource)
    resource_group_str = json.dumps(resource_group_dict, indent=2) if isinstance(resource_group_dict, dict) else str(resource_group_dict)
    
    text = f"""
    You are a Terraform expert. Your task is to analyze the provided Terraform module code and update it according to the specified resource details.

    The module code is:
    {content}

    The resource details are:
    {resource_str}

    The resource group details are:
    {resource_group_str}

    Below is the cloud provider:
    {cloud_provider}

    File name being processed:
    {file_name}

    Please ensure the following:
    1. Update the module code to match the provided resource details.
    2. Ensure the resource group is correctly referenced.
    3. Maintain proper Terraform syntax and best practices.
    4. Return only the updated Terraform code without any additional explanation.
    """

    # print("*" * 20)
    # print("Azure prompt:\n", text)
    # print("*" * 20)
    
    try:
        endpoint = "https://devops-maf1.openai.azure.com/"
        deployment = "gpt-4.1-nano"
        subscription_key = model_subscription_key
        api_version = "2024-12-01-preview"

        if not subscription_key:
            return "Error: AZURE_OPENAI_KEY not found in environment variables"

        azure_client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=subscription_key,
        )

        response = azure_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful Terraform expert assistant.",
                },
                {
                    "role": "user",
                    "content": text,
                }
            ],
            max_tokens=10000,
            temperature=0.7,
            model=deployment
        )

        # print("Azure response:.................\n")
        # print(response.choices[0].message.content)
        # print("=" * 20)
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Azure Error: {str(e)}")
        return f"Azure Error: {str(e)}"

def github_read_contents(path, repo_owner=REPO_OWNER, repo_name="Terraform_modules"):
    """Read file content from GitHub repository"""
    try:
        print(f"Reading content from path: {path}")
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        content = repo.get_contents(path)
        decoded_content = content.decoded_content.decode()
        print(f"Successfully read content from {path}")
        return decoded_content
    except Exception as e:
        print(f"Error reading GitHub file content from {path}: {e}")
        return None

def github_find_folder(cloud, resource_type, repo_owner=REPO_OWNER, repo_name="Terraform_modules"):
    """Find terraform module files in GitHub repo with path modules/{cloud}/{resource_type}"""
    try:
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        tree = repo.get_git_tree("HEAD", recursive=True).tree

        target_path = f"modules/{cloud}/{resource_type}"
        
        found_paths = []
        for item in tree:
            if item.path.startswith(target_path):
                # Only include files (blob type), not folders (tree type)
                if item.type == 'blob':
                    found_paths.append(item.path)

        print(f"Total module files found for {cloud}/{resource_type}: {len(found_paths)}")
        print("Found files:", found_paths)
        print("=" * 30)
        return found_paths
        
    except Exception as e:
        print(f"Error searching GitHub repo: {e}")
        return []

def create_terraform_files_dict(files_to_push):
    """Convert files to the format expected by github_push_files"""
    # Based on yaml_tools implementation, github_push_files expects:
    # files_to_push: dict with file_path as key and file_content as value
    return files_to_push

""""Version 3"""
@tool(name="TF_Module_builder", description="Builds Terraform modules by understanding the requirements such as the desired infrastructure, cloud provider, and specific configurations.", approval_mode="never_require")
async def TF_Module_builder(
    repo_name: Annotated[str, Field(description="The name of the repository for which the infrastructure should be provisioned")],
    cloud_provider: Annotated[str, Field(description="The cloud provider to be used for the infrastructure (e.g., 'azure', 'aws', 'gcp')")],
    Resources: Annotated[str, Field(description="""ALL resources to be provisioned in a SINGLE JSON structure. Example:
                                                {
                                                  "vm": {
                                                    "name": "my-vm",
                                                    "size": "Standard_B1ms",
                                                    "ram": "2GB"
                                                  },
                                                  "webapp": {
                                                    "name": "my-webapp", 
                                                    "port": 80,
                                                    "location": "East US"
                                                  },
                                                  "resource_group": {
                                                    "name": "rg-main",
                                                    "location": "East US"
                                                  }
                                                }
                                                Resource names should be lowercase with underscores.""")]):
    print("Building Terraform configuration...")
    print("Cloud Provider:", cloud_provider)
    print("Resources:", Resources)
    
    try:
        # Parse resources if it's a string
        if isinstance(Resources, str):
            resources_dict = json.loads(Resources)
        else:
            resources_dict = Resources

        print("Parsed Resources Dictionary:", resources_dict)

        # Extract resource group information
        resource_group_dict = resources_dict.get("resource_group", {})
        
        # Get other resources (excluding resource_group)
        other_resources_dict = {
            k: v for k, v in resources_dict.items() if k != "resource_group"
        }

        print("Resource Group:", resource_group_dict)
        print("Other Resources:", other_resources_dict)

        # Dictionary to store all files to be pushed
        files_to_push = {}
        processed_resources = []

        # Process each resource type
        for resource_type, resource_config in other_resources_dict.items():
            print(f"\n=== Processing {resource_type} ===")
            
            # Get all file paths for this resource type
            paths = github_find_folder(cloud_provider, resource_type)
            
            if not paths:
                print(f"No modules found for {resource_type}")
                continue

            # Process each file for this resource type
            for path in paths:
                try:
                    print(f"Processing path: {path}")
                    
                    # Read file content
                    content = github_read_contents(path)
                    if not content:
                        print(f"No content found for {path}")
                        continue

                    # Extract file information
                    file_name = path.split("/")[-1]  # e.g., "main.tf"
                    
                    print(f"Processing file: {file_name}")

                    # Process different file types
                    if file_name == "variables.tf":
                        print(f"Calling Azure AI for {file_name}")
                        
                        try:
                            updated_content = get_azure_response(
                                content=content,
                                file_name=file_name,
                                cloud_provider=cloud_provider,
                                resource_group_dict=resource_group_dict,
                                resource=resource_config
                            )
                            
                            if updated_content and not updated_content.startswith("Azure Error:"):
                                # Create proper folder structure: repo-name/resource-type/file
                                target_path = f"{repo_name}/{resource_type}/{file_name}"
                                files_to_push[target_path] = updated_content
                                
                                print(f"Prepared {target_path} for deployment (processed by AI)")
                            else:
                                print(f"Azure AI returned error for {file_name}: {updated_content}")
                                
                        except Exception as azure_error:
                            print(f"Error calling Azure AI for {file_name}: {azure_error}")
                            continue
                            
                    elif file_name in ["main.tf", "outputs.tf"]:
                        print(f"Directly pushing {file_name} without AI processing")
                        
                        # Create proper folder structure: repo-name/resource-type/file
                        target_path = f"{repo_name}/{resource_type}/{file_name}"
                        files_to_push[target_path] = content
                        
                        print(f"Prepared {target_path} for deployment (direct push)")
                        
                    elif file_name == "README.md":
                        print(f"Skipping {file_name} as it does not require processing")
                        
                    else:
                        print(f"Skipping file: {file_name} (unknown file type)")

                except Exception as file_error:
                    print(f"Error processing file {path}: {file_error}")
                    import traceback
                    traceback.print_exc()
                    continue

            processed_resources.append(resource_type)

        # Push all files to the target repository
        if files_to_push:
            print(f"\nPushing {len(files_to_push)} files to repository: {repo_name}")
            
            # Display what will be pushed with proper folder structure
            for file_path in files_to_push.keys():
                print(f"  - {file_path}")
            
            try:
                commit_message = f"Add Terraform modules for {', '.join(processed_resources)} on {cloud_provider}"
                github_push_files(
                    files_to_push=files_to_push,
                    commit_message=commit_message,
                    branch="main"
                )
                
                print(f"Successfully pushed all files to {repo_name}")
                
            except Exception as push_error:
                print(f"Error pushing files to repository: {push_error}")
                return f"ERROR: Failed to push files to repository - {str(push_error)}"
        else:
            print("No files to push")

        return f"TASK COMPLETED: Successfully generated and deployed Terraform configuration for {cloud_provider} with resources: {processed_resources}. Total files pushed to repository {repo_name}: {len(files_to_push)}"

    except json.JSONDecodeError as json_error:
        print(f"JSON parsing error: {json_error}")
        return f"ERROR: Invalid JSON format in Resources parameter - {str(json_error)}"
    
    except Exception as e:
        print("Exception Received:", str(e))
        import traceback
        traceback.print_exc()
        return f"ERROR: Failed to generate Terraform configuration - {str(e)}"