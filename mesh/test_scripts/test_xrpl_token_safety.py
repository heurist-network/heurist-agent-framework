import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mesh.agents.xrpl_token_safety_agent import XrplTokenSafetyAgent

ISSUER = "rMxCKbEDwqr76QuheSUMdEGf4B9xJ8m5De"
CURRENCY = "524C555344000000000000000000000000000000"


class TokenSafetyTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.agent = XrplTokenSafetyAgent()
        self.agent._catalog = AsyncMock(return_value=[{
            "issuer": ISSUER, "currency": CURRENCY, "score": 55,
            "flags": ["one", "two", "three", "four"], "as_of": 1,
            "slug": "rlusd-rMxCKbED-a364197ffb",
        }])

    async def asyncTearDown(self):
        await self.agent.cleanup()
        del self.agent

    async def check(self, issuer=ISSUER, currency="RLUSD"):
        return await self.agent._handle_tool_logic("check_token_safety", {"issuer": issuer, "currency": currency})

    async def test_snapshot_and_encoded_links(self):
        result = await self.check()
        self.assertEqual(result["score"], 55)
        self.assertEqual(result["flags"], ["one", "two", "three"])
        self.assertTrue(result["stale"])
        self.assertEqual(result["currency"], CURRENCY)
        self.assertIn("currency=" + CURRENCY, result["report_url"])

    async def test_hex_currency(self):
        self.assertEqual((await self.check(currency=CURRENCY.lower()))["score"], 55)

    async def test_issuer_identity_not_ticker(self):
        self.assertIn("error", await self.check(issuer="rp2DskzVGGz6iDw8ViSVjcMabqJJ2wA2S6"))

    async def test_currency_case_preserved(self):
        self.assertIn("error", await self.check(currency="rlusd"))

    async def test_bad_input_no_network(self):
        self.assertIn("error", await self.check(issuer="https://example.com"))
        self.agent._catalog.assert_not_awaited()

    async def test_upstream_failure_not_safe_result(self):
        self.agent._catalog.side_effect = RuntimeError("unavailable")
        with self.assertRaises(RuntimeError):
            await self.check()

    async def test_unknown_tool(self):
        self.assertIn("error", await self.agent._handle_tool_logic("buy", {}))
        self.agent._catalog.assert_not_awaited()


if __name__ == "__main__":
    unittest.main()
