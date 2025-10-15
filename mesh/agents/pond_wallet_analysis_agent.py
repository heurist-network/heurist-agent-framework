import logging
import os
from typing import Any, Dict, List, Optional

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)


class PondWalletAnalysisAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("POND_API_KEY")
        if not self.api_key:
            raise ValueError("POND_API_KEY environment variable is required")

        self.base_url = "https://broker-service.private.cryptopond.xyz"
        self.headers = {"Content-Type": "application/json"}
        self.model_ids = {
            "ethereum": 20,
            "base": 16,
        }

        self.metadata.update(
            {
                "name": "Pond Wallet Analysis Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent analyzes cryptocurrency wallet activities across Ethereum and Base networks using the Cryptopond API.",
                "external_apis": ["Cryptopond"],
                "tags": ["Wallet Analysis"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/CryptoPond.png",
                "examples": [
                    "Analyze Ethereum wallet 0x2B25B37c683F042E9Ae1877bc59A1Bb642Eb1073",
                    "What's the trading volume for Ethereum wallet 0x2B25B37c683F042E9Ae1877bc59A1Bb642Eb1073?",
                    "Check the transaction activity for Base wallet 0x97224Dd2aFB28F6f442E773853F229B3d8A0999a",
                ],
                "credits": 0,
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                },
            }
        )

    def get_system_prompt(self) -> str:
        return """Analyze crypto wallet activity on Ethereum or Base chain. Focus on trading volume, transaction count, gas fees, token diversity, profit and loss, and behavioral patterns over time.

            Identify trends such as accumulation, selling pressure, inactivity, or sudden activity spikes. Pay attention to timing, frequency, and consistency in wallet behavior.

            Present data clearly by formatting large numbers (e.g., 48.5M), emphasizing key insights, and flagging any unusual or suspicious activity.

            Ensure the wallet address format matches the target network (e.g., 0x for Ethereum/Base). Always report missing or incomplete data, and base conclusions strictly on what's available without assumptions."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "analyze_ethereum_wallet",
                    "description": "Analyze an Ethereum wallet address for DEX trading frequency and volume and PnL over the last 30 days. The unit of gas fees is in GWEI. Useful when analyzing trading patterns of an EOA wallet.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "address": {
                                "type": "string",
                                "description": "Ethereum wallet address (starts with 0x)",
                            },
                        },
                        "required": ["address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_base_wallet",
                    "description": "Analyze a Base network wallet address for DEX trading frequency and volume and PnL over the last 30 days. Ignore the gas fee results. Useful when analyzing trading patterns of an EOA wallet.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "address": {
                                "type": "string",
                                "description": "Base wallet address (starts with 0x)",
                            },
                        },
                        "required": ["address"],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                      CRYPTOPOND API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=3600)
    @with_retry(max_retries=3)
    async def analyze_wallet(self, address: str, network: str) -> Dict:
        """Analyze a wallet on a specified network."""
        model_id = self.model_ids.get(network)
        if not model_id:
            return {"error": f"Unsupported network: {network}"}

        payload = {
            "req_type": "1",
            "access_token": self.api_key,
            "input_keys": [address],
            "model_id": model_id,
        }

        result = await self._api_request(
            url=f"{self.base_url}/predict", method="POST", headers=self.headers, json_data=payload
        )
        if "error" in result:
            return result

        if result.get("code") != 200 or "resp_items" not in result:
            return {"error": f"API returned unexpected response: {result}"}

        resp_items = result.get("resp_items", [])
        if not resp_items or "analysis_result" not in resp_items[0]:
            return {"error": "No analysis results found in response"}

        return {
            "network": network,
            "address": address,
            "analysis": resp_items[0]["analysis_result"],
            "updated_at": resp_items[0].get("debug_info", {}).get("UPDATED_AT"),
        }

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Dispatch tool requests based on tool name."""
        address = function_args.get("address")
        if not address:
            return {"error": "Missing 'address' parameter"}

        tool_map = {
            "analyze_ethereum_wallet": ("ethereum", True),
            "analyze_base_wallet": ("base", True),
        }

        tool = tool_map.get(tool_name)
        if not tool:
            return {"error": f"Unsupported tool: {tool_name}"}

        network, requires_0x = tool

        if requires_0x and not address.startswith("0x"):
            return {"error": f"Invalid {network.capitalize()} address format. Address should start with '0x'"}

        address = address.lower() if requires_0x else address
        logger.info(f"Analyzing {network.capitalize()} wallet: {address}")

        result = await self.analyze_wallet(address, network)

        if errors := self._handle_error(result):
            return errors

        return result
