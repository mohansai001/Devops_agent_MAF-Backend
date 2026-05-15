from openai import AzureOpenAI #type: ignore
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import google.generativeai as genai #type: ignore
import time
from utils.config import Content_generator_model_config as cgconfig

def get_azure_response(text):
    try:
        endpoint = cgconfig.AI_content_endpoint
        deployment = cgconfig.AI_content_model
        subscription_key = cgconfig.AI_content_key
        api_version = cgconfig.AI_content_version
        # print(endpoint, deployment, subscription_key, api_version)

        if not subscription_key:
            return "Error: AZURE_OPENAI_KEY not found in environment variables"
 
        client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=subscription_key,
        )
 
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
            max_tokens=5000,
            temperature=0.9,
            model=deployment
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Azure Error: {str(e)}"

if __name__ == "__main__":
    print(get_azure_response("Hello, how are you?"))