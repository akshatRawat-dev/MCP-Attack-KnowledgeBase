import asyncio
import logging
from dotenv import load_dotenv
import os

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

load_dotenv()

logging.basicConfig(
    filename="client.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    filemode="a",  
)

logger = logging.getLogger(__name__)

print("SSLKEYLOGFILE=",os.environ.get("SSLKEYLOGFILE"))

async def main():
    async with MCPServerStreamableHttp(
        params={
            "url": "http://localhost:8000/mcp",
        }
    ) as mcp_server:

        agent = Agent(
            name="MCP Assistant",
            model="gpt-3.5-turbo",
            instructions="""

You are an intelligent assistant connected to an MCP server.

Use MCP tools when they are appropriate for the user's request.

When the user requests information from a file or external data
source, retrieve and process that information using the appropriate
MCP tool.

Do not guess tool results.
""",
            mcp_servers=[mcp_server],
        )

        print("MCP HTTP Client started.")
        print("Type 'exit' to stop.\n")

        while True:
            user_input = input("You: ")

            if user_input.lower() in ("exit", "quit"):
                logger.info("Client exited.")
                break

            logger.info("User: %s", user_input)

            try:
                result = await Runner.run(agent, user_input)

                print("\nAssistant:")
                print(result.final_output)
                print()

                logger.info("Assistant: %s", result.final_output)

            except Exception:
                logger.exception("Error while running agent")


if __name__ == "__main__":
    asyncio.run(main())