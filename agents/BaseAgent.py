from agent_framework import Agent #type: ignore
from utils.clientConnection import get_client
from agent_framework.exceptions import ChatClientException #type: ignore
import asyncio
from utils.config import Base_agent_config as baconfig
# from agent_framework.middleware import SecurityAgentMiddleware #type: ignore

class BaseAgent:
    _instance = None
    name = None
    model = baconfig.model or "gpt-4.1-nano"
    AI_endpoint = baconfig.AI_endpoint or "https://devops-maf1.cognitiveservices.azure.com/api/projects/proj-default"
    instructions = None
    tools = []
    context_providers = []
    agent_middleware = []
    run_middleware = []
    debug_context = False

    def __init__(self):
        self._agent = Agent(
            client=get_client(model=self.model, endpoint=self.AI_endpoint),
            name=self.name,
            instructions=self.instructions,
            tools=self.tools,
            context_providers=self.context_providers,
            middleware=self.agent_middleware
        )
        self._session = self._agent.create_session()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # async def run(self, prompt: str):
    async def run(self, prompt: str, retries: int = 2):
        try:
            for attempt in range(retries + 1):
                try:
                    return await self._agent.run(prompt,
                                                session=self._session,
                                                middleware=self.run_middleware)
                except ChatClientException as e:
                    if "Azure CLI" in str(e) and attempt < retries:
                        print(f"Azure CLI not ready, retrying in 2s... (attempt {attempt + 1})")
                        await asyncio.sleep(2)
                    else:
                        raise
        finally:
            await self._clear_session()
        # return await self._agent.run(prompt)

    # async def _clear_session(self):
    #     for provider in self.context_providers:
    #         if hasattr(provider, "clear"):
    #             await provider.clear()
    async def _clear_session(self):
        if self.debug_context:
            await self._print_context()
        for provider in self.context_providers:
            if hasattr(provider, "clear") and not getattr(provider, "persist_across_sessions", False):
                await provider.clear()

    async def _print_context(self):
        print(f"\n{'='*60}")
        print(f"[{self.name}] Session Context Before Clear")
        print(f"{'='*60}")

        state = self._session.state

        for provider in self.context_providers:
            source_id = getattr(provider, "source_id", provider.__class__.__name__)
            print(f"\n--- {provider.__class__.__name__} (source_id: '{source_id}') ---")

            messages = state.get(source_id, {}).get("messages", [])

            if not messages:
                print(f"  (no messages)")
                continue

            for msg in messages:
                role = getattr(msg, "role", "?")
                contents = getattr(msg, "contents", [])

                print(f"\n  [{role}]")
                for content in contents:
                    ctype = getattr(content, "type", "unknown")

                    if ctype == "text":
                        # plain text — user messages, assistant responses
                        print(f"    text       : {content.text}")

                    elif ctype == "function_call":
                        # sub-agent tool call — what the coordinator requested
                        print(f"    tool_call  : {content.name}({str(getattr(content, 'arguments', ''))})")

                    elif ctype == "function_result":
                        # sub-agent response — what came back
                        print(f"    tool_result: {str(getattr(content, 'result', content))}")

                    else:
                        # catch-all for reasoning, data, etc.
                        print(f"    [{ctype}]: {str(content)}")

        print(f"\n{'='*60}\n")