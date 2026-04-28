from agents.co_ordinator_agent import co_ordinator
import asyncio

response = asyncio.run(co_ordinator.run("GET DEMO ci pipeline"))
print(response)
