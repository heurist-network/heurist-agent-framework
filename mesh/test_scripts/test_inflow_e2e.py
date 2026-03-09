"""End-to-end test: Inflow payment flow through /mesh_request."""

import json
import os
import sys
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
load_dotenv(project_root / ".env")

MESH_URL = os.getenv("MESH_SERVER_URL", "http://localhost:8000")
BUYER_USER_ID = os.environ["INFLOW_USER_ID"]

RETRY_INTERVAL = 5
MAX_RETRIES = 60


def pp(label: str, resp: httpx.Response):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"  Status: {resp.status_code}")
    print(f"{'='*60}")
    try:
        print(json.dumps(resp.json(), indent=2))
    except Exception:
        print(resp.text[:1000])


def main():
    with httpx.Client(base_url=MESH_URL, timeout=30) as client:
        # Step 1: First call — no request_id → should create Inflow payment request
        body = {
            "agent_id": "TokenResolverAgent",
            "input": {
                "tool": "token_profile",
                "tool_arguments": {"coingecko_id": "bitcoin"},
                "raw_data_only": True,
            },
            "payment": {
                "provider": "INFLOW",
                "user_id": BUYER_USER_ID,
                "currency": "USDC",
            },
        }
        r = client.post("/mesh_request", json=body)
        pp("Step 1: First call (create payment request)", r)

        if r.status_code != 200:
            print("\n  First call failed. Check buyer wallet has sufficient funds.")
            return

        resp = r.json()
        request_id = resp.get("payment", {}).get("request_id")
        if not request_id:
            print("\n  [!] No request_id in response")
            return

        print(f"\n  -> Got request_id: {request_id}")
        print("\n  Please approve the payment in Inflow dashboard/email/mobile.")
        print(f"  Polling every {RETRY_INTERVAL}s (max {MAX_RETRIES} attempts)...")

        # Step 2: Poll with the request_id until approved or terminal failure
        body["payment"]["request_id"] = request_id
        for attempt in range(1, MAX_RETRIES + 1):
            time.sleep(RETRY_INTERVAL)
            r = client.post("/mesh_request", json=body)
            resp = r.json()
            status = resp.get("status")

            if status == "payment_pending":
                print(f"  Attempt {attempt}: still pending...")
                continue

            if status == "payment_not_approved":
                pp(f"Step 2: Payment declined/expired (attempt {attempt})", r)
                return

            # Tool result returned — success
            pp(f"Step 2: Tool executed successfully (attempt {attempt})", r)
            return

        print(f"\n  Timed out after {MAX_RETRIES} attempts. Payment was not approved in time.")


main()
