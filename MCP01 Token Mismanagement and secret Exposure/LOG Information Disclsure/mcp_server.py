import logging
import requests
from pathlib import Path

from fastmcp import FastMCP


mcp = FastMCP("Payment Processing Service")

PAYMENT_API = "http://127.0.0.1:8003/api/payments"
LOG_ENDPOINT = "http://127.0.0.1:8003/api/logs"

# ---------------------------------------------------------
# LOCAL LOG FILE
# ---------------------------------------------------------

PAYMENT_LOG_FILE = Path("payment.log")

# Create the log file if it does not already exist.
PAYMENT_LOG_FILE.touch(exist_ok=True)


logging.basicConfig(
    filename=str(PAYMENT_LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("payment_processor")


def process_transaction(payment_data):

    return {
        "status": "processed",
        "payment_id": int(payment_data["payment_id"]),
        "amount": float(payment_data["amount"]),
        "currency": payment_data["currency"]
    }



def process_payment(payment_data):

    log_message = (
        f"Processing payment: {payment_data}"
    )

    # Write complete payment data to local log.
    logger.info(log_message)

    print("[+] Log written to payment.log")

    try:

        response = requests.post(
            LOG_ENDPOINT,
            json={
                "event": "payment_processing",
                "message": log_message,
                "payment_data": payment_data
            },
            timeout=5
        )

        response.raise_for_status()

        print(
            "[+] Log successfully transferred to Flask"
        )

        print(
            "[+] Flask response:",
            response.json()
        )

    except requests.RequestException as error:

        print(
            "[!] Failed to transfer log:"
        )

        print(
            f"[!] {error}"
        )

    return process_transaction(payment_data)


@mcp.tool()
def process_payment_by_id(payment_id: int) -> dict:

    """
    Process a payment using its payment ID.
    Retrieves a payment record and processes
    the transaction.
    
    PAYMENT_API = "http://127.0.0.1:8003/api/payments/{payment_id}"

    and send all the logs to server 
    LOG_ENDPOINT = "http://127.0.0.1:8003/api/logs"
    """

    response = requests.get(
        f"{PAYMENT_API}/{payment_id}",
        timeout=5
    )

    response.raise_for_status()

    payment_data = response.json()

    return process_payment(payment_data)


if __name__ == "__main__":
     mcp.run(
            transport="streamable-http",
            host="0.0.0.0",
            port=8002
        )