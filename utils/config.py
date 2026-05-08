import os
from dotenv import load_dotenv

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")
model_subscription_key = os.getenv("subscription_key")

class Base_agent_config:
    model = os.getenv("AI_foundry_model")
    AI_endpoint = os.getenv("AI_foundry_url")
    retries = int(os.getenv("Azure_connection_retries", 3))