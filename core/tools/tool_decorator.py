import inspect
from typing import Any, Callable, Dict


def tool(description: str):
    """
    A decorator factory that creates a tool decorator with a specified description.
    """

    def decorator(func):
        # Add metadata to the function
        func.name = func.__name__
        func.description = func.__doc__ if func.__doc__ != inspect._empty else description

        # generate the parameter schema without agent_context
        func.is_async = inspect.iscoroutinefunction(func)
        signature = inspect.signature(func)
        func.is_ctx_required = "agent_context" in signature.parameters

        # Map Python types to valid JSON Schema types
        type_mapping = {
            "str": "string",
            "int": "number",
            "float": "number",
            "bool": "boolean",
            "list": "array",
            "dict": "object",
            "NoneType": "null",
        }

        parameters = {k: v for k, v in signature.parameters.items() if k != "agent_context"}
        func.args_schema = {
            "type": "object",
            "properties": {
                param: {
                    "type": type_mapping.get(str(param_type.annotation.__name__).lower(), "string"),
                    "description": str(param_type.annotation)
                    if param_type.annotation != inspect._empty
                    else "No type specified",
                }
                for param, param_type in parameters.items()
            },
            "required": [param for param, param_type in parameters.items() if param_type.default == inspect._empty],
        }

        async def wrapper(args: Dict[str, Any], agent_context: Any):
            # re-add agent context
            if func.is_ctx_required:
                args["agent_context"] = agent_context
            result = await func(**args) if func.is_async else func(**args)
            return result

        wrapper.name = func.name
        wrapper.description = func.description
        wrapper.args_schema = func.args_schema
        wrapper.original = func

        return wrapper

    return decorator


def convert_to_function_schema(func: Callable) -> Dict[str, Any]:
    """
    Converts a decorated function into an OpenAI function schema format.
    """
    return {
        "type": "function",
        "function": {"name": func.name, "description": func.description, "parameters": func.args_schema},
    }


def get_tool_schemas(tools: list[Callable]) -> list[Dict[str, Any]]:
    """
    Convert a list of tool-decorated functions into OpenAI function schemas.

    Args:
        tools: List of functions decorated with @tool

    Returns:
        List of function schemas in OpenAI format
    """
    return [convert_to_function_schema(tool) for tool in tools]
