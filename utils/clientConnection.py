from agent_framework.foundry import FoundryChatClient #type: ignore
from azure.identity import AzureCliCredential #type: ignore

# credential = AzureCliCredential()
# client = FoundryChatClient(
#     project_endpoint="https://devops-maf1.cognitiveservices.azure.com/api/projects/proj-default",
#     model="gpt-4.1-nano",
#     credential=credential,
# )

# from agent_framework.foundry import FoundryChatClient
# from azure.identity import AzureCliCredential

_client = None

def get_client():
    global _client
    if _client is None:
        credential = AzureCliCredential()
        _client = FoundryChatClient(
            project_endpoint="https://devops-maf1.cognitiveservices.azure.com/api/projects/proj-default",
            model="gpt-4.1-nano",
            credential=credential,
        )
    return _client