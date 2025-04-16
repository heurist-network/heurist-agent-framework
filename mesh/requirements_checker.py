import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from mesh.mesh_manager import AgentLoader, Config  # noqa: E402

if __name__ == "__main__":
    print("\n== Testing Agent Imports ==")
    config = Config()
    agent_loader = AgentLoader(config)

    try:
        agents_dict = agent_loader.load_agents()
        num_agents = len(agents_dict)
        print(f"✅ Successfully loaded {num_agents} agents")
    except Exception:
        print("❌ Failed to load agents")
