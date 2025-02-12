from typing import Dict, Any, Optional
import logging
import os
from mesh_agent import MeshAgent, monitor_execution, with_retry, with_cache
from core.llm import call_llm_async

logger = logging.getLogger(__name__)

class ProtocolResolverAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update({
            'name': 'Protocol Resolver Agent',
            'version': '1.0.0',
            'author': 'Heurist Team',
            'author_address': '0x7d9d1821d15B9e0b8Ab98A058361233E255E405D',
            'description': 'Resolves protocol names to IDs and provides protocol information',
            'inputs': [
                {
                    'name': 'query',
                    'description': 'Natural language query about a protocol',
                    'type': 'str'
                },
                {
                    'name': 'protocol_id',
                    'description': 'Direct protocol ID input',
                    'type': 'str'
                }
            ],
            'outputs': [
                {
                    'name': 'response',
                    'description': 'Natural language description of the protocol',
                    'type': 'str'
                },
                {
                    'name': 'data',
                    'description': 'Raw protocol data',
                    'type': 'dict'
                }
            ],
            'tags': ['Protocol', 'DeFi']
        })

        self.protocol_mapping = {
            "uniswap-v3": {
                "name": "Uniswap V3",
                "category": "DEX",
                "chains": ["ethereum", "polygon", "arbitrum", "optimism"],
                "description": "Automated market maker with concentrated liquidity"
            },
            "aave-v3": {
                "name": "Aave V3",
                "category": "Lending",
                "chains": ["ethereum", "polygon", "avalanche", "arbitrum"],
                "description": "Decentralized lending protocol"
            }
        
        }

    @monitor_execution()
    @with_cache(ttl_seconds=3600)
    async def resolve_protocol_id(self, query: str) -> Optional[str]:
        """Use LLM to resolve protocol name to ID"""
        if not query:
            return None

        system_prompt = f"""Given a user query about a protocol, identify which protocol they are referring to from this list: {str(self.protocol_mapping)}
Return only the protocol ID (key) if found, or 'unknown' if no match. Be flexible with variations in naming."""

        try:
            response = await call_llm_async(
                base_url=self.heurist_base_url,
                api_key=self.heurist_api_key,
                model_id=self.large_model_id,
                system_prompt=system_prompt,
                user_prompt=query,
                temperature=0.1
            )
            
            resolved_id = response.strip().lower()
            if resolved_id in self.protocol_mapping:
                return resolved_id
            return None
            
        except Exception as e:
            logger.error(f"Error in protocol resolution: {str(e)}")
            return None

    @monitor_execution()
    @with_retry(max_retries=3)
    async def handle_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming message with either query or protocol_id"""
        query = params.get('query')
        protocol_id = params.get('protocol_id')

        if not query and not protocol_id:
            raise ValueError("Either query or protocol_id must be provided")

        if query and not protocol_id:
            protocol_id = await self.resolve_protocol_id(query)
            if not protocol_id:
                return {
                    "response": f"Could not resolve protocol from query: {query}",
                    "data": None
                }

        protocol_data = self.protocol_mapping.get(protocol_id)
        if not protocol_data:
            return {
                "response": f"Protocol ID not found: {protocol_id}",
                "data": None
            }

        system_prompt = """You are a DeFi protocol expert. Given protocol data, generate a concise but informative 
        description of the protocol, including its category, supported chains, and key features."""
        
        natural_response = await call_llm_async(
            base_url=self.heurist_base_url,
            api_key=self.heurist_api_key,
            model_id=self.large_model_id,
            system_prompt=system_prompt,
            user_prompt=str(protocol_data),
            temperature=0.7
        )

        return {
            "response": natural_response,
            "data": protocol_data
        }