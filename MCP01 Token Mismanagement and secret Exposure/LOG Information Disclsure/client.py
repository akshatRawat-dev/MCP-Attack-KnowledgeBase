import os
import ssl

import asyncio
import httpx
from dotenv import load_dotenv
from openai import AsyncOpenAI

from agents import Agent, Runner, set_default_openai_client
from agents.mcp import MCPServerStreamableHttp

load_dotenv()

KEYLOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sslkeys.log")
ssl_ctx = ssl.create_default_context()
ssl_ctx.keylog_filename = KEYLOG

openai_client = AsyncOpenAI(http_client=httpx.AsyncClient(verify=ssl_ctx))
set_default_openai_client(openai_client)

print(f"SSL key log: {KEYLOG}")


async def main():
    async with MCPServerStreamableHttp(
        params={
            "url": "http://localhost:8002/mcp",
        },
        cache_tools_list=True,
    ) as mcp_server:

        await mcp_server.list_tools()

        agent = Agent(
            name="MCP Client",
            model="gpt-4o-mini",
            instructions="""
You are an assistant connected to an MCP server.
Use MCP tools automatically whenever they are useful.
Do not guess tool results.
""",
            mcp_servers=[mcp_server],
        )

        print("MCP HTTP Client started.")
        print("Type 'exit' to stop.\n")

        while True:
            user_input = input("You: ")

            if user_input.lower() in ("exit", "quit"):
                break

            try:
                result = await Runner.run(agent, user_input)

                print("\nAssistant:")
                print(result.final_output)
                print()

            except Exception as e:
                print(f"[error] {e}")


if __name__ == "__main__":
    asyncio.run(main())
