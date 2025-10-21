import sys
from abc import ABC
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from typing import Dict, Type

from dotenv import load_dotenv
from loguru import logger

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from mesh.mesh_agent import MeshAgent  # noqa: E402

logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
)


class Config:
    """Minimal configuration wrapper to ensure environment variables are loaded."""

    def __init__(self):
        load_dotenv()


class AgentLoader:
    """Handles dynamic loading of agent modules."""

    def __init__(self, config: Config):
        self.config = config

    def load_agents(self) -> Dict[str, Type[MeshAgent]]:
        agents_dict: Dict[str, Type[MeshAgent]] = {}
        package_name = "mesh.agents"
        found_agents = []
        import_errors = []

        try:
            package = import_module(package_name)
            package_path = Path(package.__file__).parent

            for _, module_name, is_pkg in iter_modules([str(package_path)]):
                if is_pkg:
                    continue

                full_module_name = f"{package_name}.{module_name}"
                try:
                    mod = import_module(full_module_name)
                    for attr_name in dir(mod):
                        attr = getattr(mod, attr_name)
                        if isinstance(attr, type) and issubclass(attr, MeshAgent) and attr is not MeshAgent:
                            # Skip abstract classes
                            if ABC in attr.__bases__ or getattr(attr, "__abstractmethods__", set()):
                                continue
                            try:
                                _ = attr()
                                agents_dict[attr.__name__] = attr
                                found_agents.append(f"{attr.__name__} ({module_name})")
                            except Exception as e:
                                logger.error(f"Unexpected error processing module {module_name}: {e}", exc_info=True)
                                continue
                except ImportError as e:
                    import_errors.append(f"{module_name}: {str(e)}")
                    continue
                except Exception as e:
                    import_errors.append(f"{module_name}: Unexpected error: {str(e)}")
                    continue

            if found_agents:
                logger.info(f"Found agents: {', '.join(found_agents)}")
            if import_errors:
                logger.warning(f"Import errors: {', '.join(import_errors)}")

            return agents_dict
        except Exception as e:
            logger.exception(f"Critical error loading agents: {str(e)}")
            return {}
