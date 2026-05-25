import yaml
from typing import Tuple, Optional


def validate_yaml(yaml_content: str) -> Tuple[bool, Optional[str]]:
    """
    Validates YAML syntax.

    Args:
        yaml_content (str): YAML content as string.

    Returns:
        Tuple[bool, Optional[str]]:
            - True, None -> if YAML is valid
            - False, error_message -> if YAML is invalid
    """

    try:
        yaml.safe_load(yaml_content)
        return True, None

    except yaml.YAMLError as e:
        return False, str(e)

    except Exception as e:
        return False, f"Unexpected Error: {str(e)}"


# Example Usage
if __name__ == "__main__":

    valid_yaml = """
    name: CI Pipeline
    on:
      push:
        branches:
          - main

    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - name: Checkout
            uses: actions/checkout@v4
    """

    invalid_yaml = """
    name: CI Pipeline
      on:
        push:
    """

    is_valid, error = validate_yaml(valid_yaml)

    if is_valid:
        print("YAML is valid")
    else:
        print("YAML is invalid")
        print(error)

    print("-" * 50)

    is_valid, error = validate_yaml(invalid_yaml)

    if is_valid:
        print("YAML is valid")
    else:
        print("YAML is invalid")
        print(error)