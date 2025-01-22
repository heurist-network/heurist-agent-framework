import sys
from pathlib import Path
import yaml
import re

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.zkignite_yield_agent import ZkIgniteYieldAgent
import asyncio

def get_next_version(script_dir: Path, base_filename: str) -> int:
    pattern = f"{base_filename}.v(\\d+).yaml"
    existing_versions = []
    
    for file in script_dir.glob(f"{base_filename}.v*.yaml"):
        match = re.match(pattern, file.name)
        if match:
            version_num = int(match.group(1))
            existing_versions.append(version_num)
        return max(existing_versions, default=0) + 1

async def run_agent():
    agent = ZkIgniteYieldAgent()
    try:
        result = await agent.handle_message({})
        
        script_dir = Path(__file__).parent
        base_filename = f"{agent.__class__.__name__.lower()}_example"
        version = get_next_version(script_dir, base_filename)
        output_file = script_dir / f"{base_filename}.v{version}.yaml"

        yaml_content = {
            'response': result['response']
        }
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)
            
        print(f"Results saved to {output_file}")
        
    finally:
        await agent.cleanup()

if __name__ == "__main__":
    asyncio.run(run_agent())
