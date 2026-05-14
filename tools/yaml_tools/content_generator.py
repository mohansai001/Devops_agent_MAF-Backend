from utils.logger import get_logger
from utils.llm import get_azure_response
from utils.preprocess import clean_yaml_output

logger = get_logger(__name__)

def create_yaml_scripts(instructions):
    logger.info("[create_yaml_scripts] Called.")
    print("[create_yaml_scripts] Called.")
    # logger.debug(f"[create_yaml_scripts] Instructions: {instructions}")
    # print(f"[create_yaml_scripts] Instructions: {instructions}")
    try: 

        response =get_azure_response(instructions)
        logger.info("[create_yaml_scripts] Azure response received.")
        # print("Azure response:\n", response,"================")
        clean_yaml = clean_yaml_output(response)
        # logger.debug(f"[create_yaml_scripts] Clean YAML: {clean_yaml}")
        print("=========================")
        return clean_yaml

    except Exception as e:
        logger.error(f"[create_yaml_scripts] Azure Error: {str(e)}", exc_info=True)
        print(f"Azure Error: {str(e)}")
        return f"Azure Error: {str(e)}"

