from typing import Dict, Any
from .mesh_agent import MeshAgent, monitor_execution, with_retry, with_cache
from core.llm import call_llm_async
from clients.merkl_client import MerklClient
import os
from dotenv import load_dotenv

load_dotenv()

# TODO: use the model that is specified in the config
MODEL_ID = "nvidia/llama-3.1-nemotron-70b-instruct"

base_url = os.getenv('HEURIST_BASE_URL')
api_key = os.getenv('HEURIST_API_KEY')

system_prompt = '''You are a professional DeFi analyst. Based on the raw data list provided by the user, generate a concise and comprehensive overview of top 10 yield opportunities on ZKsync Era. These projects are participants of ZKIgnite program, which streams 300M ZK tokens over 9 months to DeFi users who provide liquidity for key token pairs, supply to lending markets, and trade on selected DeFi protocols. Each item in the list is a yield opportunity, which may be a DEX liquidity pool, or a lending market where user can supply assets to earn yields.

Requirements:
- Report the yield opportunities with the highest APR. Read APR info from 'aprRecord' field. Rank by APR
- One protocol might have multiple yield opportunities, you should consider all of them as separate items
- Do not aggregate opportunities of the same protocol. You should compare the APR of each opportunity, not based on the protocol
- Only consider those opportunities with ZKsync token as the reward token (check 'rewardsRecord' field)
- Accurately describe how user can earn yield, which is included in the 'name' field of each opportunity. If it contains details, mention the detailed action item and the specific token(s) to be provided if applicable
- Use professional financial analysis language
- Structure the analysis in clear paragraphs
- Do not mention any aspects other than the APR of the protocols. For example, no need to mention the reward token.
- Do not do math, just use the data provided
- You just need to generate the report, do not include any other information
- You must follow the data source provided, and do not make up any data
'''

def is_zk_rewards(item):
    """Check if an opportunity has ZK token rewards"""
    ZK_TOKEN_ADDRESS = "0x5A7d6b2F92C77FAD6CCaBd7EE0624E64907Eaf3E".lower()
    
    rewards_record = item.get('rewardsRecord', {})
    breakdowns = rewards_record.get('breakdowns', [])
    
    for breakdown in breakdowns:
        token = breakdown.get('token', {})
        if (
            token.get('name') == 'ZKsync' or 
            token.get('address', '').lower() == ZK_TOKEN_ADDRESS
        ):
            return True
    return False

class ZkIgniteYieldAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update({
            'name': 'ZKsync Ignite Yield Analyst',
            'version': '1.0.0',
            'author': 'Heurist Team',
            'author_address': '0x7d9d1821d15B9e0b8Ab98A058361233E255E405D',
            'description': 'Analyze yield opportunities of ZKsync Ignite program.',
            'inputs': [],
            'outputs': [
                {
                    'name': 'response',
                    'description': 'The analysis result of the yield opportunities, describing the top pools, their APR, and how to earn yield',
                    'type': 'string'
                },
                {
                    'name': 'data',
                    'description': 'The data of the yield opportunities, including the protocol name, opportunity name, APR, and the specific tokens to be provided',
                    'type': 'list'
                }
            ],
            'external_apis': ['merkl']
        })
        self._api_clients['merkl'] = MerklClient()

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    async def get_opportunities(self, chain_id: str, items: int) -> Dict:
        return await self._api_clients['merkl'].get_opportunities(chain_id=chain_id, items=items)
    
    @monitor_execution()
    @with_retry(max_retries=3)
    async def handle_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        data_to_analyze = []
        data_to_return = []
        base_data = await self.get_opportunities(chain_id="324", items=100)
        for item in base_data:
            if 'protocol' not in item:
                continue
            if item['status'] != 'LIVE':
                continue

            if not is_zk_rewards(item):
                continue
            # important: only select those fields that are needed
            data_to_analyze.append({
                'protocol_name': item['protocol']['name'],
                'opportunity_name': item['name'],
                'apr': item['apr'],
                'rewardsRecord': item['rewardsRecord'],
                'protocol_icon': item['protocol']['icon']
            })
            tokens = []
            if item['tokens']:
                for token in item['tokens']:
                    tokens.append({
                        'id': token['id'],
                        'icon': token['icon'],
                    })
            protocol = {
                'name': item['protocol']['name'],
                'icon': item['protocol']['icon'],
            }
            
            data_to_return.append({
                'name': item['name'].replace('Provide liquidity to ', '').replace('Supply ', '').replace(' ', '\n'),
                'protocol': protocol,
                'tvl': item['tvl'],
                'apr': item['apr'],
                'status': item['status'],
                'dailyRewards': item['dailyRewards'],
                'tokens': tokens
            })

        analysis_result = await call_llm_async(
            base_url=base_url,
            api_key=api_key,
            model_id=MODEL_ID,
            system_prompt=system_prompt,
            user_prompt=data_to_analyze,
            temperature=0.1
        )
        return {
            'response': analysis_result,
            'data': data_to_return
        }