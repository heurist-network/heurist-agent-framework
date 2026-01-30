import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from decorators import with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()

# Mode configuration for next_step instructions
MODE_CONFIG = {
    "normal": {"initial_wait": 60, "poll_interval": 30},
    "deep": {"initial_wait": 120, "poll_interval": 60},
}


class AskHeuristAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_API_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_API_KEY environment variable is required")

        self.base_url = "https://ask-backend.heurist.xyz"
        self.headers = {"X-HEURIST-API-KEY": self.api_key, "Content-Type": "application/json"}

        self.metadata.update(
            {
                "name": "Ask Heurist Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Crypto Q&A and research agent for traders. Ask questions about token analysis, market trends, trading strategies, macro news, and get in-depth analysis. Website: https://ask.heurist.ai",
                "external_apis": ["Ask Heurist"],
                "tags": ["Research", "Trading"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/AskHeurist.png",
                "examples": [
                    "What is the current price of Bitcoin?",
                    "Give me a market digest for today",
                    "What are the latest crypto news?",
                    "Should I buy ETH right now? (deep mode)",
                ],
                "verified": True,
                "recommended": True,
                "credits": 10,
                "x402_config": {
                    "enabled": True,
                    "tool_prices": {"ask_heurist": "0.1", "check_job_status": "0.001"},
                },
                "erc8004": {
                    "enabled": True,
                    "supported_trust": ["reputation"],
                    "wallet_chain_id": 1,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return """You are a crypto Q&A and research assistant powered by Ask Heurist.

You have two tools:
1. ask_heurist: Submit a crypto question. Returns a job_id immediately. Supports two modes:
   - "normal" (default): For token prices, news, market digest (2 credits, ~1 min)
   - "deep": For complex analysis, trading advice (10 credits, 2-3 min)
2. check_job_status: Check the status of a job by its ID to retrieve the result

Workflow: Call ask_heurist to submit a question, then use check_job_status after the recommended wait time to get the result."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "ask_heurist",
                    "description": "Submit a crypto question to Ask Heurist. Returns a job_id immediately. Use check_job_status after the recommended wait time to retrieve the result.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "The crypto question or research query to ask.",
                            },
                            "mode": {
                                "type": "string",
                                "enum": ["normal", "deep"],
                                "default": "normal",
                                "description": "Query mode: 'normal' for quick answers (prices, news), 'deep' for complex analysis.",
                            },
                        },
                        "required": ["prompt"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "check_job_status",
                    "description": "Check the status of an Ask Heurist job by its ID. Returns the result if completed, or next_step instructions if still pending.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "job_id": {
                                "type": "string",
                                "description": "The job ID returned by ask_heurist.",
                            }
                        },
                        "required": ["job_id"],
                    },
                },
            },
        ]

    async def ask_heurist(self, prompt: str, mode: str = "normal") -> Dict[str, Any]:
        """Submit a crypto question to Ask Heurist and return job_id immediately."""
        if mode not in MODE_CONFIG:
            mode = "normal"

        config = MODE_CONFIG[mode]
        logger.info(f"Submitting Ask Heurist query (mode={mode}): {prompt[:50]}...")

        url = f"{self.base_url}/api/v1/internal/jobs"
        payload = {"prompt": prompt, "mode": mode}

        response = await self._api_request(url=url, method="POST", headers=self.headers, json_data=payload, timeout=30)

        if response.get("error"):
            logger.error(f"Ask Heurist API error: {response['error']}")
            return {"error": response["error"]}

        job_id = response.get("job_id")
        if not job_id:
            logger.error("No job_id returned from Ask Heurist API")
            return {"error": "Failed to create job"}

        logger.info(f"Job created: {job_id}")

        return {
            "job_id": job_id,
            "prompt": prompt,
            "mode": mode,
            "next_step": f"Call check_job_status with job_id '{job_id}' after {config['initial_wait']} seconds to retrieve the result.",
        }

    async def check_job_status(self, job_id: str) -> Dict[str, Any]:
        """Check the status of an existing job by its ID."""
        logger.info(f"Checking job status for ID: {job_id}")

        url = f"{self.base_url}/api/v1/internal/jobs/{job_id}"
        response = await self._api_request(url=url, method="GET", headers=self.headers, timeout=30)

        if response.get("error"):
            logger.error(f"Ask Heurist API error: {response['error']}")
            return {"error": response["error"]}

        job_status = response.get("status")
        logger.info(f"Job {job_id} status: {job_status}")

        if job_status == "completed":
            return {
                "job_status": job_status,
                "job_id": job_id,
                "prompt": response.get("prompt"),
                "result_text": response.get("result_text", ""),
                "share_url": response.get("share_url", ""),
            }

        if job_status == "failed":
            error_msg = response.get("error", "Job failed")
            logger.error(f"Job {job_id} failed: {error_msg}")
            return {"error": f"Job failed: {error_msg}"}

        # Still pending
        return {
            "job_status": job_status,
            "job_id": job_id,
            "prompt": response.get("prompt"),
            "next_step": f"Job is still {job_status}. Call check_job_status again after 30 seconds.",
        }

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name == "ask_heurist":
            prompt = function_args.get("prompt")
            if not prompt:
                return {"error": "Missing 'prompt' parameter"}

            mode = function_args.get("mode", "normal")
            return await self.ask_heurist(prompt, mode)

        elif tool_name == "check_job_status":
            job_id = function_args.get("job_id")
            if not job_id:
                return {"error": "Missing 'job_id' parameter"}

            return await self.check_job_status(job_id)

        else:
            return {"error": f"Unsupported tool: {tool_name}"}
