from .BaseAgent import BaseAgent
from .yaml_agent import yaml_agent
from .github_agent import github_agent
from .tf_agent import terraform_agent
from utils.prompt_manager_v2 import AgentInstructionPrompt
from agent_framework import InMemoryHistoryProvider #type: ignore

class CoOrdinatorAgent(BaseAgent):
    name = "Co_ordinator"
    debug_context = True
    instructions = str(AgentInstructionPrompt("co-ordinator-instructions"))
    tools = [yaml_agent, github_agent, terraform_agent]
    context_providers = [
        InMemoryHistoryProvider(load_messages=True),
        InMemoryHistoryProvider("audit", load_messages=False, store_context_messages=True),
    ]
# instruction = PromptManager()

# co_ordinator = Agent(
#     client=client,
#     name="Co_ordinator",
#     instructions=instruction.format("co_ordinator_instructions"),
#     tools=[yaml_agent, github_agent]
# )

