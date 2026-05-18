from agent_framework.foundry import FoundryChatClient #type: ignore
from azure.identity import AzureCliCredential #type: ignore
from azure.core.credentials import TokenRequestOptions #type:ignore
from azure.identity import DefaultAzureCredential #type: ignore
from azure.identity import ManagedIdentityCredential, AzureCliCredential, ChainedTokenCredential #type: ignore
from typing import Annotated
from pydantic import Field

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

_clients: dict = {}

def _get_credential():
    # Uses Managed Identity in Azure, falls back to CLI locally
    _credential = DefaultAzureCredential(
                    exclude_cli_credential=True,
                    exclude_visual_studio_code_credential=True,
                    exclude_shared_token_cache_credential=True,
                )
    return _credential

def get_client(
    model: Annotated[str, Field(default="gpt-4.1-nano", description="AI foundry model used.")],
    endpoint: Annotated[str, Field(default="https://devops-maf1.cognitiveservices.azure.com/api/projects/proj-default", description="AI foundry endpoint URL.")]
) -> FoundryChatClient:
    key = (model, endpoint)
    if key not in _clients:
        _clients[key] = FoundryChatClient(
            project_endpoint=endpoint,
            model=model,
            credential=_get_credential(),
        )
    return _clients[key]