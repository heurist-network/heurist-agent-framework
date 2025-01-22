import sys
from pathlib import Path
import yaml

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.zkignite_yield_agent import ZkIgniteYieldAgent
import asyncio

async def run_agent():
    agent = ZkIgniteYieldAgent()
    try:
        agent_input = {}
        agent_output = await agent.handle_message({})
        
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            'input': agent_input,
            'output': agent_output
        }
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)
            
        print(f"Results saved to {output_file}")
        
    finally:
        await agent.cleanup()

if __name__ == "__main__":
    asyncio.run(run_agent())
