"""
PQS (Prompt Quality Score) Agent

Scores any LLM prompt for quality using the PQS API. Returns a grade (A-F),
score out of 80, percentile, top 3 actionable fixes, and the 3 weakest
dimensions. Uses an 8-dimension rubric based on PEEM, RAGAS, G-Eval, and
MT-Bench frameworks.

No API key required — calls the free mesh-tier endpoint at
https://pqs.onchainintel.net/api/mesh/score
"""

import logging
from typing import Any, Dict, List, Optional

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)

PQS_MESH_URL = "https://pqs.onchainintel.net/api/mesh/score"

VALID_VERTICALS = [
    "software", "content", "business", "education",
    "science", "crypto", "general", "research",
]


class PqsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update(
            {
                "name": "PQS Prompt Quality Score",
                "version": "1.0.0",
                "author": "OnChainIntel",
                "author_address": "0xD2DfC5796de622E08C13f3016E92cfa15Ea33D0F",
                "description": (
                    "Score any LLM prompt for quality using PQS (Prompt Quality Score). "
                    "Returns a grade (A-F), score out of 80, percentile, top 3 actionable "
                    "fixes, and the 3 weakest dimensions. Uses an 8-dimension rubric based "
                    "on PEEM, RAGAS, G-Eval, and MT-Bench frameworks."
                ),
                "external_apis": ["PQS"],
                "tags": ["AI", "Prompt Engineering", "Quality"],
                "image_url": "https://pqs.onchainintel.net/pqs-logo.png",
                "examples": [
                    "Score this prompt: Write me a blog post about AI",
                    "How good is this prompt for software engineering: Build a REST API with Node.js that handles user authentication",
                    "Rate my prompt: Explain quantum computing to a 5 year old using analogies",
                    "Check prompt quality: As a senior data scientist, analyze this CSV dataset and provide insights on customer churn patterns, including a confusion matrix and ROC curve",
                ],
            }
        )

    # ------------------------------------------------------------------
    #                        SYSTEM PROMPT
    # ------------------------------------------------------------------
    def get_system_prompt(self) -> str:
        return (
            "You are a prompt quality analyst powered by PQS (Prompt Quality Score). "
            "Your role is to help users understand and improve the quality of their LLM prompts.\n\n"
            "When a user provides a prompt to score, extract the prompt text from their message "
            "and call the score_prompt tool. Present the results clearly:\n"
            "- State the grade and score (e.g. 'Grade C — 34/80, 43rd percentile')\n"
            "- List the 3 weakest dimensions with a one-line explanation of what each means\n"
            "- Present the top fixes as actionable next steps the user can apply immediately\n"
            "- If the score is below 48/80 (grade C or lower), emphasize that significant improvement is possible\n\n"
            "If the user asks a general question about prompt quality without providing a specific prompt, "
            "give brief guidance and ask them to share a prompt to score.\n\n"
            "Available verticals for domain-specific scoring: software, content, business, education, "
            "science, crypto, general, research. Default to 'general' unless the user's prompt is "
            "clearly about one of these domains."
        )

    # ------------------------------------------------------------------
    #                        TOOL SCHEMAS
    # ------------------------------------------------------------------
    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "score_prompt",
                    "description": (
                        "Score any LLM prompt for quality using PQS. Returns grade (A-F), "
                        "score out of 80, percentile, top 3 actionable fixes, and the 3 weakest "
                        "dimensions of the prompt."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "The LLM prompt to score for quality",
                            },
                            "vertical": {
                                "type": "string",
                                "enum": VALID_VERTICALS,
                                "description": (
                                    "Domain context for scoring. Defaults to 'general'. "
                                    "Use 'software' for code prompts, 'crypto' for blockchain, etc."
                                ),
                            },
                        },
                        "required": ["prompt"],
                    },
                },
            }
        ]

    # ------------------------------------------------------------------
    #                        API CALL
    # ------------------------------------------------------------------
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=1)
    async def _score_prompt(self, prompt: str, vertical: str = "general") -> Dict[str, Any]:
        """Call the PQS mesh endpoint and return the raw result."""
        result = await self._api_request(
            url=PQS_MESH_URL,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-Heurist-Agent": "PqsAgent/1.0.0",
            },
            json_data={"prompt": prompt, "vertical": vertical},
            timeout=30,
        )

        if isinstance(result, dict) and "error" in result:
            return {"status": "error", "error": result["error"]}

        return {"status": "success", "data": result}

    # ------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle execution of specific tools and return the raw data."""
        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name != "score_prompt":
            return {"error": f"Unsupported tool: {tool_name}"}

        prompt = function_args.get("prompt")
        if not prompt:
            return {"error": "Missing 'prompt' parameter"}

        vertical = function_args.get("vertical", "general")
        if vertical not in VALID_VERTICALS:
            vertical = "general"

        result = await self._score_prompt(prompt=prompt, vertical=vertical)

        if errors := self._handle_error(result):
            return errors

        return result
