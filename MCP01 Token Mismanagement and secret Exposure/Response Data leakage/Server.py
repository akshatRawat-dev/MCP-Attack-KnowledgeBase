import requests
from fastmcp import FastMCP

mcp = FastMCP("MCP Lab")

CUSTOMER_API = "http://127.0.0.1:8003/api/customers"


@mcp.tool()
def get_customer(customer_id: int) -> dict:
    """
    Retrieve customer information using customer_id from the 
    customer database API: http://127.0.0.1:8003/api/customers/{customer_id}.
    """

    response = requests.get(
        f"{CUSTOMER_API}/{customer_id}",
        timeout=5
    )

    response.raise_for_status()

    customer_data = response.json()

    return customer_data


if __name__ == "__main__":
    mcp.run(
            transport="streamable-http",
            host="0.0.0.0",
            port=8000
        )