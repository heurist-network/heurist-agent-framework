import logging, os, json, re, urllib.request, ssl, asyncio
from typing import Any, Dict, List
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)

class ContentSafetyAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update({
            "name": "Content Safety Agent",
            "version": "1.0.0",
            "author": "Sichen",
            "author_address": "0x51d22f7b333CE89043A76b24aDC3Ef7a7726AED7",
            "description": "Analyzes text for AI-generated patterns, hallucinated references, and content safety issues. Helps verify if content is human-written or AI-generated.",
            "tags": ["Safety", "AI Detection", "Content", "Verification"],
            "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/main/mesh/images/default.png",
            "verified": True,
            "recommended": True,
            "examples": [
                "Check this article for AI-generated content",
                "Verify if these references are real",
                "Analyze this text for hallucination patterns",
                "Is this content human-written or AI-generated?"
            ],
            "credits": {"default": 0.3},
            "x402_config": {"enabled": True, "default_price_usd": "0.003"},
            "erc8004": {"enabled": True, "supported_trust": ["reputation"], "wallet_chain_id": 1},
        })

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "check_missing_references",
                    "description": "Analyze text and extract all references, then flag those that look like plausible-sounding but potentially fabricated sources.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "description": "The text to analyze. Include enough context for reference extraction."}
                        },
                        "required": ["text"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "detect_ai_patterns",
                    "description": "Analyze text for common AI writing patterns. Returns a risk score and specific flagged patterns.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "description": "The text to analyze for AI patterns"}
                        },
                        "required": ["text"]
                    }
                }
            },
        ]

    def get_system_prompt(self) -> str:
        return (
            "You are a content safety specialist. You help users identify AI-generated content, "
            "hallucinated references, and fabricated claims. Use your tools to analyze text and "
            "flag potential issues. Be specific about what you find."
        )

    async def _handle_tool_logic(self, tool_name: str, function_args: dict, session_context=None) -> Dict:
        if tool_name == "check_missing_references":
            return self._check_refs(function_args)
        elif tool_name == "detect_ai_patterns":
            return self._detect_ai(function_args)
        return {"status": "error", "error": f"Unknown tool: {tool_name}"}

    def _check_refs(self, args: dict) -> Dict:
        text = args.get("text", "")
        if not text:
            return {"error": "No text provided"}

        # Extract potential references
        refs = []

        # arXiv papers
        arxiv = re.findall(r'arxiv\.org/(?:abs/|pdf/)?(\d{4}\.\d{4,5})', text)
        for a in arxiv:
            refs.append({"type": "arXiv", "id": a, "url": f"https://arxiv.org/abs/{a}"})

        # GitHub repos
        github = re.findall(r'github\.com/([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)', text)
        for g in github:
            refs.append({"type": "GitHub", "id": g, "url": f"https://github.com/{g}"})

        # URLs
        urls = re.findall(r'https?://[^\s\'\")\]]+', text)
        for u in urls:
            if "arxiv.org" in u or "github.com" in u:
                continue
            refs.append({"type": "URL", "url": u[:120]})

        # Author citations like (Author, 2024) or Author et al.
        citations = re.findall(r'\(([A-Z][a-z]+(?:\s+(?:et\s+al\.|&\s+[A-Z][a-z]+))?,\s*\d{4})\)', text)
        for c in citations:
            refs.append({"type": "citation", "text": c})

        return {
            "status": "ok",
            "total_references_found": len(refs),
            "references": refs,
            "note": "AI models often fabricate plausible-sounding arXiv IDs, GitHub repos, and author citations. Verify each reference manually."
        }

    def _detect_ai(self, args: dict) -> Dict:
        text = args.get("text", "")
        if not text:
            return {"error": "No text provided"}

        flags = []
        score = 0

        # Common AI patterns
        patterns = [
            (r'in recent years|in recent months|in recent weeks', "Generic time reference lacking specificity", 2),
            (r'it is important to note that|it is worth noting that', "Padding phrase", 1),
            (r'as an AI language model|as a large language model', "Self-identifying as AI", 5),
            (r'I cannot|I apologize|I do not have access to', "AI refusal pattern", 3),
            (r'as of my last training data|as of my knowledge cutoff', "Training data reference", 4),
            (r'in the rapidly evolving landscape|in the ever-changing world', "Generic AI booster phrase", 1),
            (r'let me clarify|let me be clear|let me explain', "Transition phrase", 1),
            (r'it goes without saying|needless to say|it should be noted that', "Filler phrase", 1),
            (r'harness the power|unlock the potential|game-changer|revolutionary', "Overused marketing-speak", 2),
            (r'we can see that|as we can see|as we have seen', "Generic transition", 1),
        ]

        for pattern, reason, weight in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                flags.append({"pattern": pattern, "reason": reason, "count": len(matches), "weight": weight})
                score += weight * len(matches)

        # Suspicious reference patterns
        fake_refs = re.findall(r'\b\w+ et al\. \(\d{4}\)', text)
        if fake_refs:
            flags.append({
                "pattern": "author citation",
                "reason": f"Found {len(fake_refs)} in-text citations that may be fabricated",
                "count": len(fake_refs),
                "weight": 3,
            })
            score += 3 * len(fake_refs)

        # Determine risk level
        risk = "low"
        if score >= 10: risk = "high"
        elif score >= 4: risk = "medium"
        else: risk = "low"

        return {
            "status": "ok",
            "ai_generation_score": score,
            "risk_level": risk,
            "flags": flags,
            "summary": f"Risk level: {risk.upper()}. Score: {score}. {len(flags)} pattern(s) detected."
        }
