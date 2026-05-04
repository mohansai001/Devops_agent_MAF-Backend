from .BaseAgent import BaseAgent
from .yaml_agent import yaml_agent
from .github_agent import github_agent
from utils.prompt_manager import PromptManager

class CoOrdinatorAgent(BaseAgent):
    name = "Co_ordinator"
    instructions = PromptManager().format("co-ordinator-instructions")
    tools = [yaml_agent, github_agent]
# instruction = PromptManager()

# co_ordinator = Agent(
#     client=client,
#     name="Co_ordinator",
#     instructions=instruction.format("co_ordinator_instructions"),
#     tools=[yaml_agent, github_agent]
# )

