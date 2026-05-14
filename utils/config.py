import os
from dotenv import load_dotenv

load_dotenv()

github_token = os.getenv("RAG_GITHUB_TOKEN")
hari_github_token = os.getenv("HARI_GITHUB_TOKEN")
model_subscription_key = os.getenv("subscription_key")
AZURE_AI_API_KEY = os.getenv("subscription_key")


class Base_agent_config:
    model = os.getenv("AI_foundry_model")
    AI_endpoint = os.getenv("AI_foundry_url")
    retries = int(os.getenv("Azure_connection_retries", 3))
    AI_foundry_key = os.getenv("AI_foundry_key")

class Content_generator_model_config:
    AI_content_version = os.getenv("AI_content_version")
    AI_content_endpoint = os.getenv("AI_content_endpoint")
    AI_content_key = os.getenv("AI_content_key")
    AI_content_model = os.getenv("AI_content_model")

class DataBase_config:
    cloud_db = os.getenv("CLOUD_DB_URL")

class Azure_config:
    client_id = os.getenv("AZURE_CLIENT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")
    tenant_id = os.getenv("AZURE_TENANT_ID")
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")


#create a dictionary with Azure
azure_config = {
    "client_id": Azure_config.client_id,
    "client_secret": Azure_config.client_secret,
    "tenant_id": Azure_config.tenant_id,
    "subscription_id": Azure_config.subscription_id
}
