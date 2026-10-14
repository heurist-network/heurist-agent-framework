import logging, os, json, re, urllib.request, ssl, asyncio
from typing import Any, Dict, List, Optional
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)

class FactCheckAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update({
            "name": "Fact Check Agent",
            "version": "1.0.0",
            "author": "Sichen",
            "author_address": "0x51d22f7b333CE89043A76b24aDC3Ef7a7726AED7",
            "description": "Verifies factual claims and references in AI-generated text. Checks if cited GitHub repos, URLs, and statistics actually exist.",
            "tags": ["Verification", "Fact Check", "Research", "Quality"],
            "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/main/mesh/images/default.png",
            "verified": True,
            "recommended": True,
            "examples": [
                "The project has 5000 stars on GitHub",
                "According to a16z, AI will add 10% to GDP",
                "Check this claim: 'openagent-community/openagent has 4.8k stars'",
                "Verify the sources in this paragraph about Stable Diffusion"
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
                    "name": "verify_github_claim",
                    "description": "Verify a claim about a GitHub repository (stars, forks, description). Returns actual data vs claimed data.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "repo": {"type": "string", "description": "Repository name like 'owner/repo'"},
                            "claimed_stars": {"type": "string", "description": "Optional. The claimed star count to verify, e.g. '5000' or '4.8k'"}
                        },
                        "required": ["repo"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "verify_website_exists",
                    "description": "Check if a website URL is accessible and returns useful content.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string", "description": "The full URL to check"}
                        },
                        "required": ["url"]
                    }
                }
            },
        ]

    def get_system_prompt(self) -> str:
        return (
            "You are a fact-checking specialist. Your job is to verify claims made in AI-generated content. "
            "Users will give you statements or paragraphs that may contain factual claims about GitHub projects, "
            "websites, statistics, or events. Use your tools to verify what's real and flag what's not. "
            "Be honest when you cannot verify something. Be clear about what's verified vs unverified."
        )

    async def _handle_tool_logic(self, tool_name: str, function_args: dict, session_context=None) -> Dict:
        if tool_name == "verify_github_claim":
            return await self._verify_github(function_args)
        elif tool_name == "verify_website_exists":
            return await self._verify_website(function_args)
        return {"status": "error", "error": f"Unknown tool: {tool_name}"}

    def _parse_k(self, val):
        if isinstance(val, (int, float)):
            return int(val)
        if isinstance(val, str):
            val = val.strip().lower().replace(",", "")
            if val.endswith("k"):
                return int(float(val[:-1]) * 1000)
            if val.endswith("万"):
                return int(float(val[:-1]) * 10000)
            return int(float(val))
        return 0

    async def _verify_github(self, args: dict) -> Dict:
        repo = args.get("repo", "").strip()
        repo = re.sub(r'https?://github\.com/', '', repo).strip("/")
        claimed = args.get("claimed_stars", "")

        try:
            ctx = ssl.create_default_context()
            req = urllib.request.Request(
                f"https://api.github.com/repos/{repo}",
                headers={"User-Agent": "Mozilla/5.0"}
            )
            resp = await asyncio.get_event_loop().run_in_executor(
                None, lambda: urllib.request.urlopen(req, timeout=10, context=ctx)
            )
            data = json.loads(resp.read())
            actual_stars = data.get("stargazers_count", 0)

            result = {
                "status": "ok",
                "repo_exists": True,
                "full_name": data.get("full_name", repo),
                "actual_stars": actual_stars,
                "description": (data.get("description") or "")[:150],
                "language": data.get("language", "unknown"),
                "last_push": data.get("pushed_at", "")[:10],
            }

            if claimed:
                claimed_num = self._parse_k(claimed)
                diff = abs(claimed_num - actual_stars)
                if diff > 0:
                    result["claimed_stars"] = claimed
                    result["match"] = diff == 0
                    result["discrepancy"] = f"Claimed {claimed} but actual is {actual_stars} (diff: ±{diff})"
                else:
                    result["claimed_stars"] = claimed
                    result["match"] = True
                    result["discrepancy"] = None

            return result

        except urllib.error.HTTPError as e:
            if e.code == 404:
                return {"status": "ok", "repo_exists": False, "full_name": repo}
            return {"status": "error", "error": f"GitHub API error: {e.code}"}
        except Exception as e:
            return {"status": "error", "error": str(e)[:80]}

    async def _verify_website(self, args: dict) -> Dict:
        url = args.get("url", "").strip()
        if not url.startswith("http"):
            url = "https://" + url
        try:
            ctx = ssl.create_default_context()
            req = urllib.request.Request(url, method="HEAD",
                headers={"User-Agent": "Mozilla/5.0"})
            resp = await asyncio.get_event_loop().run_in_executor(
                None, lambda: urllib.request.urlopen(req, timeout=10, context=ctx)
            )
            return {"status": "ok", "url": url, "accessible": True, "http_code": resp.status}
        except urllib.error.HTTPError as e:
            return {"status": "ok", "url": url, "accessible": e.code < 500, "http_code": e.code}
        except Exception as e:
            return {"status": "ok", "url": url, "accessible": False, "error": str(e)[:60]}
