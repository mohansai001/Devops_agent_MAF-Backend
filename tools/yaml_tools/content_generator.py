from utils.clientConnection import get_client
from utils.config import Base_agent_config,Content_generator_model_config
from openai import AzureOpenAI
# client = get_client(model=Content_generator_model_config.model, endpoint=Content_generator_model_config.AI_content_endpoint,api_version = "2024-05-01-preview")

def clean_yaml_output(yaml_str):
    lines = yaml_str.splitlines()
    # Remove code block markers and empty lines at the start/end
    cleaned = [line for line in lines if not line.strip().startswith("```")]
    # Optionally, strip leading/trailing blank lines
    while cleaned and not cleaned[0].strip():
        cleaned.pop(0)
    while cleaned and not cleaned[-1].strip():
        cleaned.pop()
    return "\n".join(cleaned)




def create_yaml_scripts(instructions):
    endpoint = Content_generator_model_config.AI_content_endpoint
    deployment = Content_generator_model_config.AI_content_model
    subscription_key = Content_generator_model_config.AI_content_key
    api_version = "2024-05-01-preview"
    azure_client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=subscription_key,
        )
    try: 
        response = azure_client.chat.completions.create(
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
        print("Azure response:\n", response.choices[0].message.content,"================")
        clean_yaml = clean_yaml_output(response.choices[0].message.content)
        print("=========================")
        # print("clean_yaml:\n", clean_yaml,"============")
        return clean_yaml

    except Exception as e:
        print(f"Azure Error: {str(e)}")
        return f"Azure Error: {str(e)}"
    
