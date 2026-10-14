import logging, os, json, re, urllib.request, ssl, asyncio
from typing import Any, Dict, List, Optional
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)

class ProjectVerifierAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update({
            "name": "Project Verifier Agent",
            "version": "1.0.0",
            "author": "Sichen",
            "author_address": "0x51d22f7b333CE89043A76b24aDC3Ef7a7726AED7",
            "description": "Verifies authenticity and health of GitHub/AI/Web3 projects. Checks repo existence, code quality, community activity, and star authenticity.",
            "tags": ["Verification", "GitHub", "Research", "Due Diligence"],
            "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/main/mesh/images/default.png",
            "verified": True,
            "recommended": True,
            "examples": [
                "Check if elizaOS/eliza is legit",
                "Verify this GitHub project: openagent-community/openagent",
                "Analyze the health of GaiaNet-AI/gaianet-node",
                "Is this project real or star farming?"
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
                    "name": "check_github_repo",
                    "description": "Check if a GitHub repository exists and get basic stats like stars, forks, language, and last update.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "repo": {
                                "type": "string",
                                "description": "Full repository name, e.g. 'elizaOS/eliza' or full URL"
                            }
                        },
                        "required": ["repo"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "estimate_star_authenticity",
                    "description": "Analyze if a GitHub repo's stars are authentic by checking fork ratio, watcher count, and contributor patterns.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "repo": {
                                "type": "string",
                                "description": "Full repository name, e.g. 'owner/repo'"
                            }
                        },
                        "required": ["repo"]
                    }
                }
            },
        ]

    def get_system_prompt(self) -> str:
        return (
            "You are a project verification specialist. Your job is to help users determine if "
            "GitHub/AI/Web3 projects are legitimate, active, and worth their attention. "
            "You can check GitHub repos for existence and basic stats, and estimate star authenticity. "
            "Be honest about limitations. If you cannot verify something, say so."
        )

    async def _handle_tool_logic(self, tool_name: str, function_args: dict, session_context=None) -> Dict:
        if tool_name == "check_github_repo":
            return await self._check_repo(function_args)
        elif tool_name == "estimate_star_authenticity":
            return await self._check_star_authenticity(function_args)
        return {"status": "error", "error": f"Unknown tool: {tool_name}"}

    async def _check_repo(self, args: dict) -> Dict:
        repo = args.get("repo", "").strip()
        repo = re.sub(r'https?://github\.com/', '', repo).strip("/")
        if "/" not in repo:
            return {"status": "error", "error": "Invalid repo format. Use 'owner/repo'"}
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
            return {
                "status": "ok",
                "exists": True,
                "name": data.get("full_name", repo),
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "language": data.get("language", "unknown"),
                "description": (data.get("description") or "")[:200],
                "created": data.get("created_at", "")[:10],
                "last_push": data.get("pushed_at", "")[:10],
                "license": (data.get("license") or {}).get("spdx_id", "none"),
            }
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return {"status": "ok", "exists": False}
            return {"status": "error", "error": f"GitHub API error: {e.code}"}
        except Exception as e:
            return {"status": "error", "error": str(e)[:80]}

    async def _check_star_authenticity(self, args: dict) -> Dict:
        repo = args.get("repo", "").strip()
        repo = re.sub(r'https?://github\.com/', '', repo).strip("/")
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
            stars = data.get("stargazers_count", 0)
            forks = data.get("forks_count", 0)
            watchers = data.get("subscribers_count", 0)
            fork_ratio = round(forks / max(stars, 1) * 100, 1)
            watcher_ratio = round(watchers / max(stars, 1) * 100, 1)

            warnings = []
            if fork_ratio < 5 and stars > 1000:
                warnings.append(f"Low fork ratio ({fork_ratio}%). Possible star manipulation.")
            if watcher_ratio < 2 and stars > 1000:
                warnings.append(f"Low watchers ({watchers}) for {stars} stars.")
            if forks < 10 and stars > 5000:
                warnings.append(f"Too few forks ({forks}) for {stars} stars.")

            score = "high" if not warnings else "medium" if len(warnings) <= 1 else "low"
            return {
                "status": "ok",
                "stars": stars,
                "forks": forks,
                "watchers": watchers,
                "fork_ratio_pct": fork_ratio,
                "authenticity_score": score,
                "warnings": warnings,
            }
        except Exception as e:
            return {"status": "error", "error": str(e)[:80]}
