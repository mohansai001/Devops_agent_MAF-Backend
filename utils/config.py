import os
from dotenv import load_dotenv

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")
model_subscription_key = os.getenv("subscription_key")
AZURE_AI_API_KEY = os.getenv("subscription_key")


class Base_agent_config:
    model = os.getenv("AI_foundry_model")
    AI_endpoint = os.getenv("AI_foundry_url")
    retries = int(os.getenv("Azure_connection_retries", 3))
    AI_foundry_key = os.getenv("AI_foundry_key")

class Content_generator_model_config:
    model=os.getenv("AI_content_model")
    AI_content_endpoint = os.getenv("AI_content_endpoint")
    AI_content_key = os.getenv("AI_content_key")
    AI_content_model = os.getenv("AI_content_model")