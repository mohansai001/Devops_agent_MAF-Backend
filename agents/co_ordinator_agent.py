from utils.clientConnection import client
from agent_framework import Agent #type: ignore
from .yaml_agent import yaml_agent


co_ordinator = Agent(
    client=client,
    name="Co_ordinator",
    instructions="You are a helpful co-ordinator. Assist appropriate tool call based on the requirement",
    tools=[yaml_agent]
)

