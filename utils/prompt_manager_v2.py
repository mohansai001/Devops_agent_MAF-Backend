from pathlib import Path
from enum import Enum
import string
import yaml 
import requests

class PromptType(Enum):
    AGENT_INSTRUCTION = "agent_instructions"
    AGENT_DESCRIPTION = "agent_descriptions"
    TOOL_DESCRIPTION = "tool_descriptions"
    USER_PROMPT = "user_prompts"
    TEST_USER_PROMPTS = "test_user_prompts"
    FIELD_DESCRIPTION = "field_descriptions"
    GENERATOR_PROMPT = "generator_prompts"
    AGENT_WRAPPER_PROMPT = "agent_wrapper_prompts"



class SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


class PromptManager:
    GITHUB_OWNER = "mohansai001"
    GITHUB_REPO = "Devops_agent_MAF-Backend"
    GITHUB_BRANCH = "main"

    def __init__(self) :
        self.cache = {}
        self._type_dirs = {pt: pt.value for pt in PromptType}

    def _github_txt_url(
        self,
        prompt_type: PromptType,
        prompt_name: str
    ) -> str:
        return (
            f"https://raw.githubusercontent.com/"
            f"{self.GITHUB_OWNER}/"
            f"{self.GITHUB_REPO}/"
            f"{self.GITHUB_BRANCH}/"
            f"prompts/{prompt_type.value}/{prompt_name}.txt"
        )

    def _github_yaml_url(
        self,
        prompt_type: PromptType,
        prompt_name: str
    ) -> str:
        return (
            f"https://raw.githubusercontent.com/"
            f"{self.GITHUB_OWNER}/"
            f"{self.GITHUB_REPO}/"
            f"{self.GITHUB_BRANCH}/"
            f"prompts/{prompt_type.value}/{prompt_name}.yaml"
        )



    def load(self, prompt_type: PromptType, prompt_name: str) -> str:
        cache_key = ("txt", prompt_type, prompt_name)

        if cache_key in self.cache:
            return self.cache[cache_key]

        url = self._github_txt_url(prompt_type, prompt_name)

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        template = response.text

        self.cache[cache_key] = template
        return template

    def load_yaml(
        self,
        prompt_type: PromptType,
        prompt_name: str
    ) -> dict:
        cache_key = ("yaml", prompt_type, prompt_name)

        if cache_key in self.cache:
            return self.cache[cache_key]

        url = self._github_yaml_url(prompt_type, prompt_name)

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = yaml.safe_load(response.text)

        self.cache[cache_key] = data
        return data

    def format(
        self,
        prompt_type: PromptType,
        prompt_name: str,
        **kwargs
    ) -> str:
        template = self.load(prompt_type, prompt_name)
        return template.format_map(kwargs)


class BasePrompt:
    _prompt_type: PromptType
    _manager = PromptManager()

    def __init__(self, name: str):
        self.name = name
        self._template = self._manager.load(self._prompt_type, name)
        self._required_keys: frozenset[str] = frozenset(       # computed ONCE
            field_name
            for _, field_name, _, _ in string.Formatter().parse(self._template)
            if field_name is not None
        )
    
    """def list_prompts(self):
        result = {}
        for pt in PromptType:
            folder = PromptManager.BASE_DIR / pt.value
            if folder.exists():
                result[pt.value] = [
                    f.stem for f in folder.iterdir()
                    if f.suffix in (".txt", ".yaml")
                ]
            else:
                result[pt.value] = []
        return result"""

    def render(self, **kwargs) -> str:
        missing = self._required_keys - kwargs.keys()          # reuses pre-computed keys
        if missing:
            raise ValueError(
                f"[{self.__class__.__name__}('{self.name}')] "
                f"Missing required variables: {sorted(missing)}. "
                f"Expected: {sorted(self._required_keys)}"
            )
        return self._manager.format(self._prompt_type, self.name, **kwargs)

    def __str__(self) -> str:
        return self._template

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"


class AgentInstructionPrompt(BasePrompt):
    """Loads from prompts/instructions/<name>.txt"""
    _prompt_type = PromptType.AGENT_INSTRUCTION


class AgentDescriptionPrompt(BasePrompt):
    """Loads from prompts/descriptions/<name>.txt"""
    _prompt_type = PromptType.AGENT_DESCRIPTION

class UserPrompt(BasePrompt):
    """Loads from prompts/user_prompts/<name>.txt"""
    _prompt_type = PromptType.USER_PROMPT

class TestUserPrompt(BasePrompt):
    """Loads from prompts/test_user_prompts/<name>.txt"""
    _prompt_type = PromptType.TEST_USER_PROMPTS

class ToolDescriptionPrompt(BasePrompt):
    """Loads from prompts/tool_descriptions/<name>.txt"""
    _prompt_type = PromptType.TOOL_DESCRIPTION

class GeneratorPrompt(BasePrompt):
    """Loads from prompts/generators/<name>.txt"""
    _prompt_type = PromptType.GENERATOR_PROMPT

class ToolFieldsPrompt:
    """
    Loads field descriptions from prompts/tool_fields/<name>.yaml
    Usage: ToolFieldsPrompt("git-commit").get("repo")
    """
    _prompt_type = PromptType.FIELD_DESCRIPTION
    _manager = PromptManager()

    def __init__(self, name: str):
        self.name = name
        self._fields: dict = self._manager.load_yaml(self._prompt_type, name)

    def get(self, field_name: str) -> str:
        if field_name not in self._fields:
            raise ValueError(
                f"[ToolFieldsPrompt('{self.name}')] "
                f"Field '{field_name}' not found. "
                f"Available: {sorted(self._fields.keys())}"
            )
        return self._fields[field_name]

    def __repr__(self) -> str:
        return f"ToolFieldsPrompt(name={self.name!r})"

# --- Usage ---
if __name__ == "__main__":
    # Load and render an instruction prompt
    # Reads from: prompts/instructions/summarize.txt
    # instruction = ToolFieldsPrompt("tf-agent-field-description")
    # print(instruction.__str__())  # Raw template

    # # Load and render a description prompt
    # # Reads from: prompts/descriptions/product.txt
    # description = DescriptionPrompt("product")
    # print(description.render(product_name="Widget Pro", price="$49"))

    # Access raw template string
    # print(instruction.get("resources"))
    text = AgentDescriptionPrompt("github-agent-description")
    # text = text.render(content = "content1", resource_str = "resource_str", resource_group_str = "resource_group_str", cloud_provider = "cloud_provider", file_name = "file_name")
    print(text)