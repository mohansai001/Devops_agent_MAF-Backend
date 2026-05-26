import yaml
from typing import Tuple, Optional
import io
import hcl2

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


def validate_hcl(hcl_content: str) -> Tuple[bool, Optional[str]]:
    """
    Validates HCL syntax.
    """
    try:
        # hcl2.load expects a file-like object
        hcl2.load(io.StringIO(hcl_content))
        return True, None
    except Exception as e:
        return False, str(e)



# Example Usage
if __name__ == "__main__":

    valid_hcl = """
    provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "East US"
}

output "resource_group_name" {
  value = azurerm_resource_group.example.name
}
    """

    invalid_hcl = """
    provider "azurerm" {
  features 
}

resource "azurerm_resource_group" "example" {
  name = "example-resources"
  location = "East US"
  # Missing closing brace below
  

output "resource_group_name" {
  value = azurerm_resource_group.example.name
}
    """

    is_valid, error = validate_hcl(valid_hcl)

    if is_valid:
        print("HCL is valid")
    else:
        print("HCL is invalid")
        print(error)

    print("-" * 50)

    is_valid, error = validate_hcl(invalid_hcl)

    if is_valid:
        print("HCL is valid")
    else:
        print("HCL is invalid")
        print(error)