import asyncio
import logging
import os
import time
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from firecrawl import FirecrawlApp

from decorators import with_cache, with_retry
from mesh.gemini import call_gemini_async
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class EtherscanAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("FIRECRAWL_API_KEY")
        if not self.api_key:
            raise ValueError("FIRECRAWL_API_KEY environment variable is required")

        self.app = FirecrawlApp(api_key=self.api_key)
        self._api_clients["firecrawl"] = self.app  # Register in base class API clients

        # Supported blockchain
        self.explorers = {
            "ethereum": "https://etherscan.io",
            "base": "https://basescan.org",
            "arbitrum": "https://arbiscan.io",
            "zksync": "https://era.zksync.network",
            "avalanche": "https://snowscan.xyz",
            "bsc": "https://bscscan.com",
        }

        self.metadata.update(
            {
                "name": "Etherscan Agent",
                "version": "1.1.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can analyze blockchain transactions, addresses, and ERC20 tokens across multiple chains using blockchain explorers and Firecrawl for data extraction.",
                "external_apis": ["Firecrawl"],
                "tags": ["Blockchain"],
                "verified": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Etherscan.png",
                "examples": [
                    "Analyze transaction 0xd8a484a402a4373221288fed84e9025ed48eba2a45a7294c19289f740ca00fcd on Ethereum",
                    "Get address history for 0x742d35Cc6639C0532fEa3BcdE3524A0be79C3b7B on Base",
                    "Show token transfers for 0x55d398326f99059ff775485246999027b3197955 on BSC",
                    "Get top holders for 0xEF22cb48B8483dF6152e1423b19dF5553BbD818b on Base",
                ],
                "credits": {"default": 1},
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                },
            }
        )

    def get_system_prompt(self) -> str:
        return """You are an intelligent blockchain data processor that extracts ALL valuable information from blockchain explorer pages.

        Strip out ALL garbage: ads, navigation, headers, footers, cookie notices, social buttons, HTML artifacts, excessive whitespace.

        Capture EVERYTHING useful: transaction actions, method calls, token transfers, internal transactions, contract interactions, event logs, multi-sig details, DeFi interactions, NFT transfers, gas data, security warnings, verification status, source code availability, special badges. Accurately represent ALL useful info present in the given data without adding subjective interpretation or missing details.

        Format clearly:
        - Make addresses clickable: [0xaddress](full_explorer_url)
        - Use **bold headers** for sections
        - Present complex data in tables
        - Keep monetary values with original units

        Focus on blockchain data only. Ignore website UI elements.
        Always include FULL list with ALL meaningful details. Avoid placeholder symbols like empty table elements in your output to save space"""

    async def _process_with_llm(self, raw_content: str, context_info: Dict[str, str]) -> str:
        """Process raw scraped content with LLM and track performance"""
        start_time = time.time()

        try:
            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                {
                    "role": "user",
                    "content": f"""Extract and format the relevant blockchain data from this {context_info.get("type", "page")} content.

                Context:
                - Chain: {context_info.get("chain", "unknown")}
                - Explorer URL: {context_info.get("url", "unknown")}
                - Data Type: {context_info.get("type", "unknown")}

                Raw Content:
                {raw_content}""",
                },
            ]

            response = await call_gemini_async(
                api_key=self.gemini_api_key,
                messages=messages,
                max_tokens=25000,
                temperature=0.1,
            )

            processed_content = response if isinstance(response, str) else response.get("content", raw_content)
            processing_time = time.time() - start_time
            logger.info(f"LLM processing completed in {processing_time:.2f}s for {context_info.get('type', 'content')}")

            return processed_content

        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"LLM processing failed after {processing_time:.2f}s: {str(e)}")
            logger.warning("Falling back to raw content due to LLM processing failure")
            return raw_content

    async def _scrape_and_process(self, url: str, context_info: Dict[str, str]) -> Dict[str, Any]:
        """Common method to scrape URL and process with LLM"""
        try:
            scrape_result = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.app.scrape_url(url, formats=["markdown"], wait_for=10000)
            )
            markdown_content = getattr(scrape_result, "markdown", "") if hasattr(scrape_result, "markdown") else ""
            if not markdown_content:
                return {"status": "error", "error": f"Failed to scrape {context_info['type']} page"}
            processed_content = await self._process_with_llm(markdown_content, context_info)
            logger.info(f"Successfully processed {context_info['type']} data")

            return {
                "status": "success",
                "data": {
                    "processed_content": processed_content,
                },
            }
        except Exception as e:
            logger.error(f"Exception in _scrape_and_process for {context_info['type']}: {str(e)}")
            return {"status": "error", "error": f"Failed to get {context_info['type']} data: {str(e)}"}

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_transaction_details",
                    "description": "Analyze a specific blockchain transaction. Provides detailed information about the transaction including sender, receiver, gas fees, and transaction actions (such as trading on DEX, interacting with DeFi). Use this tool when you want to know what exactly happened for a transaction id.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chain": {
                                "type": "string",
                                "description": "Blockchain network to query.",
                                "enum": ["ethereum", "base", "arbitrum", "zksync", "avalanche", "bsc"],
                            },
                            "txid": {
                                "type": "string",
                                "description": "Transaction hash starting with 0x",
                            },
                        },
                        "required": ["chain", "txid"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_address_history",
                    "description": "Analyze a blockchain address to get transaction history, balance, and activity summary. Use this tool to gets insights into the address usage patterns and token holdings.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chain": {
                                "type": "string",
                                "description": "Blockchain network to query",
                                "enum": ["ethereum", "base", "arbitrum", "zksync", "avalanche", "bsc"],
                            },
                            "address": {
                                "type": "string",
                                "description": "Wallet address starting with 0x",
                            },
                        },
                        "required": ["chain", "address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_erc20_token_transfers",
                    "description": "Get recent token transfer transactions and basic token information including name, symbol, total supply, and holder count. Use this tool to understand recent tranfers of the token. Do not use this for token holder detailed distribution.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chain": {
                                "type": "string",
                                "description": "Blockchain network where the token is deployed",
                                "enum": ["ethereum", "base", "arbitrum", "zksync", "avalanche", "bsc"],
                            },
                            "address": {
                                "type": "string",
                                "description": "Token contract address",
                            },
                        },
                        "required": ["chain", "address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_erc20_top_holders",
                    "description": "Get top 50 token holders data including wallet addresses, balances, percentages, and basic token information. Use this tool to understand token holder distribution.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chain": {
                                "type": "string",
                                "description": "Blockchain network where the token is deployed",
                                "enum": ["ethereum", "base", "arbitrum", "zksync", "avalanche", "bsc"],
                            },
                            "address": {
                                "type": "string",
                                "description": "Token contract address",
                            },
                        },
                        "required": ["chain", "address"],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                      ETHERSCAN API-SPECIFIC METHODS
    # ------------------------------------------------------------------------

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_transaction_details(self, chain: str, txid: str) -> Dict[str, Any]:
        """
        Scrape and analyze transaction details from blockchain explorer.
        """
        logger.info(f"Getting transaction details for {txid} on {chain}")

        if chain not in self.explorers:
            return {"status": "error", "error": f"Unsupported chain: {chain}"}

        explorer_url = self.explorers[chain]
        url = f"{explorer_url}/tx/{txid}"
        context_info = {"type": "transaction", "chain": chain, "url": url}

        return await self._scrape_and_process(url, context_info)

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_address_history(self, chain: str, address: str) -> Dict[str, Any]:
        """
        Scrape and analyze address history from blockchain explorer.
        """
        logger.info(f"Getting address history for {address} on {chain}")

        if chain not in self.explorers:
            return {"status": "error", "error": f"Unsupported chain: {chain}"}

        explorer_url = self.explorers[chain]
        url = f"{explorer_url}/address/{address}"
        context_info = {"type": "address", "chain": chain, "url": url}

        return await self._scrape_and_process(url, context_info)

    @with_cache(ttl_seconds=3600)
    @with_retry(max_retries=3)
    async def get_erc20_token_transfers(self, chain: str, address: str) -> Dict[str, Any]:
        """
        Scrape and analyze ERC20 token transfers and basic token info from blockchain explorer.
        """
        logger.info(f"Getting ERC20 token transfers for {address} on {chain}")

        if chain not in self.explorers:
            return {"status": "error", "error": f"Unsupported chain: {chain}"}

        explorer_url = self.explorers[chain]
        url = f"{explorer_url}/token/{address}"
        context_info = {"type": "token_transfers", "chain": chain, "url": url}

        return await self._scrape_and_process(url, context_info)

    @with_cache(ttl_seconds=3600)
    @with_retry(max_retries=3)
    async def get_erc20_top_holders(self, chain: str, address: str) -> Dict[str, Any]:
        """
        Scrape and analyze top 50 ERC20 token holders from blockchain explorer.
        """
        logger.info(f"Getting ERC20 top holders for {address} on {chain}")

        if chain not in self.explorers:
            return {"status": "error", "error": f"Unsupported chain: {chain}"}

        explorer_url = self.explorers[chain]
        url = f"{explorer_url}/token/{address}#balances"
        context_info = {"type": "token_holders", "chain": chain, "url": url}

        return await self._scrape_and_process(url, context_info)

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle execution of specific tools and return the processed data"""

        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name == "get_transaction_details":
            chain = function_args.get("chain")
            txid = function_args.get("txid")
            if not chain or not txid:
                return {"status": "error", "error": "Missing required parameters: chain and txid"}
            result = await self.get_transaction_details(chain, txid)

        elif tool_name == "get_address_history":
            chain = function_args.get("chain")
            address = function_args.get("address")
            if not chain or not address:
                return {"status": "error", "error": "Missing required parameters: chain and address"}
            result = await self.get_address_history(chain, address)

        elif tool_name == "get_erc20_token_transfers":
            chain = function_args.get("chain")
            address = function_args.get("address")
            if not chain or not address:
                return {"status": "error", "error": "Missing required parameters: chain and address"}
            result = await self.get_erc20_token_transfers(chain, address)

        elif tool_name == "get_erc20_top_holders":
            chain = function_args.get("chain")
            address = function_args.get("address")
            if not chain or not address:
                return {"status": "error", "error": "Missing required parameters: chain and address"}
            result = await self.get_erc20_top_holders(chain, address)

        else:
            return {"status": "error", "error": f"Unsupported tool: {tool_name}"}

        errors = self._handle_error(result)
        if errors:
            return errors

        return result
