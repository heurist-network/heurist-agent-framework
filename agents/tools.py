from typing import List, Dict, Any, Optional, Callable
import logging
import requests
import json
from .tool_decorator import get_tool_schemas
from .tool_box import ToolBox
from .tool_decorator_example import DECORATED_TOOLS_EXAMPLES

logger = logging.getLogger(__name__)

class Tools(ToolBox):
    def __init__(self):
        # Initialize the base class
        super().__init__()
        
        # Store decorated tools
        # Not necessary to as it is already stored in the ToolBox class
        # But explicitly storing it here for clarity
        self._decorated_tools: List[Callable] = self.decorated_tools
        
        # Register the decorated tools
        self.register_decorated_tools(DECORATED_TOOLS_EXAMPLES + self._decorated_tools)

    def register_decorated_tool(self, tool_func: Callable) -> None:
        """Register a decorated tool function"""
        if hasattr(tool_func, 'name') and hasattr(tool_func, 'args_schema'):
            self._decorated_tools.append(tool_func)
            self.tool_handlers[tool_func.name] = tool_func
        else:
            logger.warning(f"Tool {tool_func.__name__} is not properly decorated")

    def register_decorated_tools(self, tools: List[Callable]) -> None:
        """Register multiple decorated tools at once"""
        for tool in tools:
            self.register_decorated_tool(tool)

    def get_tools_config(self, filter_tools: List[str] = None) -> List[Dict[str, Any]]:
        """
        Get tool configurations, optionally filtered by tool names
        
        Args:
            filter_tools: Optional list of tool names to include
            
        Returns:
            List of tool configurations
        """
        all_tools = self.tools_config + get_tool_schemas(self._decorated_tools)
        
        if filter_tools:
            return [tool for tool in all_tools 
                    if tool["function"]["name"] in filter_tools]
        return all_tools

    async def execute_tool(self, tool_name: str, args: Dict[str, Any], agent_context: Any) -> Optional[Dict[str, Any]]:
        """Execute a tool by name with given arguments"""
        if tool_name not in self.tool_handlers:
            logger.error(f"Unknown tool: {tool_name}")
            return None
        result = await self.tool_handlers[tool_name](args, agent_context)
        result["tool_call"] = json.dumps({
                        "tool_call": tool_name,
                        "processed": True,
                        "args": args,
                        "result": result["result"] if "result" in result else None,
                        "data": result["data"] if "data" in result else None
                    }, default=str)
        return result


