from agent_framework.foundry import FoundryChatClient #type: ignore
from azure.identity import AzureCliCredential, ManagedIdentityCredential #type: ignore
from azure.core.credentials import TokenRequestOptions #type:ignore
from typing import Annotated
from pydantic import Field
import os

# credential = AzureCliCredential()
# client = FoundryChatClient(
#     project_endpoint="https://devops-maf1.cognitiveservices.azure.com/api/projects/proj-default",
#     model="gpt-4.1-nano",
#     credential=credential,
# )

# from agent_framework.foundry import FoundryChatClient
# from azure.identity import AzureCliCredential

_client = None
_credential = None

# def _get_credential():
#     global _credential
#     if _credential is None:
#         _credential = DefaultAzureCredential()
#         # warm up — force token fetch immediately
#         _credential.get_token("https://cognitiveservices.azure.com/.default")
#     return _credential
def get_credential():
    if os.getenv("WEBSITE_INSTANCE_ID"):
        return ManagedIdentityCredential()

    return AzureCliCredential()

def get_client(model:Annotated[str, Field(default="gpt-4.1-nano", description="AI foundry model used.")],endpoint:Annotated[str, Field(default="https://devops-maf1.cognitiveservices.azure.com/api/projects/proj-default", description="AI foundry endpoint URL.")]):
    global _client
    if _client is None:
        # credential = DefaultAzureCredential()
        _client = FoundryChatClient(
            project_endpoint=endpoint,
            model=model,
            credential= get_credential(),
        )
    return _client