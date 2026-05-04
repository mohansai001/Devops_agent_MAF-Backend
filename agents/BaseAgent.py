from agent_framework import Agent #type: ignore
from utils.clientConnection import get_client

class BaseAgent:
    _instance = None
    name = None
    instructions = None
    tools = []

    def __init__(self):
        self._agent = Agent(
            client=get_client(),
            name=self.name,
            instructions=self.instructions,
            tools=self.tools
        )

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def run(self, prompt: str):
        return await self._agent.run(prompt)