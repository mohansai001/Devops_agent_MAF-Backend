from utils.logger import get_logger

logger=get_logger(__name__)

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
    logger.debug(f"[clean_yaml_output] Cleaned YAML Output:")
    # print(f"[clean_yaml_output] Cleaned YAML: {result}")
    return result