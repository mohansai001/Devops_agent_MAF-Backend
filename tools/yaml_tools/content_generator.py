from utils.clientConnection import get_client
from utils.config import Base_agent_config,Content_generator_model_config
from openai import AzureOpenAI
from utils.logger import get_logger

logger = get_logger(__name__)

def clean_yaml_output(yaml_str):
    logger.info("[clean_yaml_output] Cleaning YAML output.")
    print("[clean_yaml_output] Cleaning YAML output.")
    lines = yaml_str.splitlines()
    # Remove code block markers and empty lines at the start/end
    cleaned = [line for line in lines if not line.strip().startswith("```")]
    # Optionally, strip leading/trailing blank lines
    while cleaned and not cleaned[0].strip():
        cleaned.pop(0)
    while cleaned and not cleaned[-1].strip():
        cleaned.pop()
    result = "\n".join(cleaned)
    logger.debug(f"[clean_yaml_output] Cleaned YAML: {result}")
    print(f"[clean_yaml_output] Cleaned YAML: {result}")
    return result




def create_yaml_scripts(instructions):
    logger.info("[create_yaml_scripts] Called.")
    print("[create_yaml_scripts] Called.")
    logger.debug(f"[create_yaml_scripts] Instructions: {instructions}")
    print(f"[create_yaml_scripts] Instructions: {instructions}")
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
        logger.info("[create_yaml_scripts] Azure response received.")
        print("Azure response:\n", response.choices[0].message.content,"================")
        clean_yaml = clean_yaml_output(response.choices[0].message.content)
        logger.debug(f"[create_yaml_scripts] Clean YAML: {clean_yaml}")
        print("=========================")
        return clean_yaml

    except Exception as e:
        logger.error(f"[create_yaml_scripts] Azure Error: {str(e)}", exc_info=True)
        print(f"Azure Error: {str(e)}")
        return f"Azure Error: {str(e)}"

