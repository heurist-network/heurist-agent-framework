import inspect
from typing import Any, Callable, Dict, Optional, Union


# ─── DACS-Standard Guardrail (§9.5.7 & §14.4) ─────────────────────────────
class DacsMandateMeta:
    def __init__(
        self,
        dacs_mandate: Optional[str] = None,
        dacs_session_id: Optional[str] = None,
        dacs_max_amount: Optional[Union[int, float, str]] = None,
    ):
        self.dacs_mandate = dacs_mandate
        self.dacs_session_id = dacs_session_id
        self.dacs_max_amount = dacs_max_amount


def assert_dacs_spend_mandate(
    requested_amount: Union[int, float, str],
    meta: Optional[Union[Dict[str, Any], DacsMandateMeta]] = None,
) -> None:
    """
    Enforces DACS-Standard §9.5.7 pre-flight spend ceiling.
    Rejects any unconstrained or over-ceiling autonomous tool execution.
    """
    if meta is None:
        return

    mandate = meta.get("dacs_mandate") if isinstance(meta, dict) else getattr(meta, "dacs_mandate", None)
    session_id = meta.get("dacs_session_id") if isinstance(meta, dict) else getattr(meta, "dacs_session_id", None)
    max_amount = meta.get("dacs_max_amount") if isinstance(meta, dict) else getattr(meta, "dacs_max_amount", None)

    if not mandate and not session_id:
        return

    if max_amount is not None:
        try:
            req_val = float(requested_amount)
            max_val = float(max_amount)
            if req_val > max_val:
                raise ValueError(
                    f"[DACS-Standard §9.5.7] Agent action aborted: requested spend ({req_val}) "
                    f"exceeds authorized mandate ceiling ({max_val})."
                )
        except (ValueError, TypeError) as e:
            if "[DACS-Standard §9.5.7]" in str(e):
                raise
            pass


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
            # DACS-Standard (§9.5.7) Pre-Flight Mandate Enforcement
            dacs_meta = args.pop("dacs_meta", None) or args.pop("dacsMeta", None)
            spend_keys = ("amount", "value", "spend_amount", "transfer_amount")
            target_amount = next(
                (args[k] for k in spend_keys if k in args and isinstance(args[k], (int, float, str))), None
            )

            if target_amount is not None and dacs_meta is not None:
                assert_dacs_spend_mandate(target_amount, dacs_meta)

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
