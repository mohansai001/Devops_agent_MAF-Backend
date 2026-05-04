from pathlib import Path

class PromptManager:
    def __init__(self, prompt_dir="prompts"):
        self.prompt_dir = Path(prompt_dir)
        self.cache = {}

    def load_template(self, prompt_name: str):
        if prompt_name in self.cache:
            return self.cache[prompt_name]

        file_path = self.prompt_dir / f"{prompt_name}.txt"

        with open(file_path, "r", encoding="utf-8") as f:
            template = f.read()

        self.cache[prompt_name] = template
        return template

    def format(self, prompt_name: str, **kwargs):
        template = self.load_template(prompt_name)
        return template.format_map(SafeDict(kwargs))


class SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"
    
def load_prompt():
    with open("prompt.txt", "r") as file:
        prompt = file.read()
    return prompt