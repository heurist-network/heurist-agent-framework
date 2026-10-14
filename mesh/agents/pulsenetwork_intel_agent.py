import os
import logging
from typing import Any, Dict, List

from dotenv import load_dotenv

from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class PulsenetworkIntelAgent(MeshAgent):
    """Token safety verdicts (8 chains incl. Robinhood Chain), Solana memecoin
    safety, and geopolitical country risk from PulseNetwork's pay-per-call
    intelligence APIs (x402-native, no signup).

    Auth: set PULSENETWORK_API_KEY. Keys are self-serve — POST
    {"contact": "you@example.com"} to
    https://pulsenetwork.theaslangroupllc.com/api/wholesale/register
    and you get a pk_live_ key with a $0.25 free-trial balance (top up with
    USDC on Base afterwards; calls fail closed to the retail x402 gate when
    the balance is exhausted).
    """

    def __init__(self):
        super().__init__()
        api_key = os.getenv("PULSENETWORK_API_KEY")
        if not api_key:
            raise ValueError("PULSENETWORK_API_KEY environment variable is required")
        self.api_key = api_key.strip()

        self.metadata.update(
            {
                "name": "PulseNetwork Intel Agent",
                "version": "1.0.0",
                "author": "PulseNetwork (The Aslan Group LLC)",
                "author_address": "0x50ab2018c06c6E4eAA9BA52057Eb55eD284912fc",
                "description": (
                    "Token safety verdicts across 8 EVM chains including Robinhood Chain "
                    "(rug/honeypot risk score with spoof-resistant liquidity checks), Solana "
                    "memecoin safety verdicts, and geopolitical country-risk briefs. Powered by "
                    "PulseNetwork — 75 x402-native intelligence APIs."
                ),
                "external_apis": ["PulseNetwork"],
                "tags": ["Security", "Geopolitics"],
                "image_url": "https://pulsenetwork.theaslangroupllc.com/logo.svg",
                "examples": [
                    "Is 0x55d398326f99059fF775485246999027B3197955 safe on BSC?",
                    "Check token safety of 0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168 on Robinhood Chain",
                    "Is this Solana memecoin a rug? AcmFHCquGwbrPxh9b3sUPMtAtXKMjkEzKnqkiHEnpump",
                    "What is the current geopolitical risk for Turkey?",
                ],
                "credits": {"default": 1},
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                },
            }
        )

        # chain slugs accepted by /api/evmtoken (robinhood = chain id 4663,
        # which the big free scanners do not expose)
        self.supported_chains = [
            "eth", "bsc", "base", "polygon", "arbitrum", "optimism", "avalanche", "robinhood",
        ]

    def get_system_prompt(self) -> str:
        return f"""You are a crypto-intelligence analyst backed by PulseNetwork data APIs.

        1. For EVM token safety questions, extract the contract address and chain
           ({", ".join(self.supported_chains)}) and call evm_token_safety.
        2. For Solana memecoin questions, extract the mint address and call
           memecoin_safety.
        3. For country/geopolitical risk questions, extract the country name and
           call country_risk.

        Report the verdict, risk score, and the concrete evidence fields returned.
        Never soften a FAIL/CAUTION verdict; state it plainly with the reasons."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "evm_token_safety",
                    "description": (
                        "Rug/honeypot safety verdict for an EVM token contract: verdict, 0-100 "
                        "risk score, one-liner, ownership/privilege checks, and spoof-resistant "
                        "liquidity analysis. Chains: " + ", ".join(
                            ["eth", "bsc", "base", "polygon", "arbitrum", "optimism", "avalanche", "robinhood"]
                        )
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "address": {"type": "string", "description": "Token contract address (0x…)"},
                            "chain": {
                                "type": "string",
                                "description": "Chain slug, e.g. eth, bsc, base, robinhood. Default eth.",
                            },
                        },
                        "required": ["address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "memecoin_safety",
                    "description": "Safety verdict for a Solana memecoin: rug risk, holder concentration, authority checks.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "mint": {"type": "string", "description": "Solana token mint address"},
                        },
                        "required": ["mint"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "country_risk",
                    "description": "Geopolitical country-risk brief: current risk drivers, stability signals, and outlook for a country.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "country": {"type": "string", "description": "Country name, e.g. Turkey"},
                        },
                        "required": ["country"],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------ #
    #                         tool implementations                        #
    # ------------------------------------------------------------------ #

    def _headers(self) -> Dict[str, str]:
        # Wholesale key: skips the x402 retail gate; each call is billed against
        # the key's prepaid balance server-side.
        return {"x-internal-key": self.api_key}

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=2)
    async def evm_token_safety(self, address: str, chain: str = "eth") -> Dict[str, Any]:
        return await self._api_request(
            url="https://onchainpulse.theaslangroupllc.com/api/evmtoken",
            method="GET",
            headers=self._headers(),
            params={"address": address, "chain": chain},
        )

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=2)
    async def memecoin_safety(self, mint: str) -> Dict[str, Any]:
        return await self._api_request(
            url="https://onchainpulse.theaslangroupllc.com/api/memecoin",
            method="GET",
            headers=self._headers(),
            params={"mint": mint},
        )

    @monitor_execution()
    @with_cache(ttl_seconds=900)
    @with_retry(max_retries=2)
    async def country_risk(self, country: str) -> Dict[str, Any]:
        return await self._api_request(
            url="https://geopoliticalpulse.theaslangroupllc.com/api/geopolitical/country-risk",
            method="GET",
            headers=self._headers(),
            params={"country": country},
        )

    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        if tool_name == "evm_token_safety":
            address = function_args.get("address")
            chain = (function_args.get("chain") or "eth").lower()
            if not address:
                return {"error": "address is required"}
            if chain not in self.supported_chains:
                return {"error": f"unsupported chain '{chain}'. Supported: {', '.join(self.supported_chains)}"}
            result = await self.evm_token_safety(address=address, chain=chain)
        elif tool_name == "memecoin_safety":
            mint = function_args.get("mint")
            if not mint:
                return {"error": "mint is required"}
            result = await self.memecoin_safety(mint=mint)
        elif tool_name == "country_risk":
            country = function_args.get("country")
            if not country:
                return {"error": "country is required"}
            result = await self.country_risk(country=country)
        else:
            return {"error": f"Unsupported tool: {tool_name}"}

        if errors := self._handle_error(result):
            return errors
        return {"status": "success", "data": result}
