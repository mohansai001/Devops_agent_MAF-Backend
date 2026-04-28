from agent_framework.foundry import FoundryChatClient #type: ignore
from azure.identity import AzureCliCredential #type: ignore

credential = AzureCliCredential()
client = FoundryChatClient(
    project_endpoint="https://devops-maf1.cognitiveservices.azure.com/api/projects/proj-default",
    model="gpt-4.1-nano",
    credential=credential,
)