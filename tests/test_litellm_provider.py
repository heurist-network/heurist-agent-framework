"""Unit tests for the LiteLLM backend in core.llm and core.components.llm_provider.

We load the two modules directly via importlib so the tests don't require the
full project dependency tree (mcp, firecrawl, psycopg2, etc.) to be installed.
"""

from __future__ import annotations

import asyncio
import importlib.util
import os
import sys
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

# ---------------------------------------------------------------------------
# Direct-file module loaders. The package __init__ pulls in many optional
# clients (firecrawl, mcp, etc.); we just want core.llm and the provider.
# ---------------------------------------------------------------------------


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _load(name: str, rel_path: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, PROJECT_ROOT / rel_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# core.llm has no internal package imports, load standalone.
llm = _load("core_llm_under_test", "core/llm.py")

# core.components.llm_provider does `from ..llm import ...`. Stub the package
# graph so the relative import resolves to the module above without dragging
# in the rest of the core package (which has heavy optional deps like
# psycopg2, firecrawl, mcp, etc.).
core_pkg = ModuleType("core_pkg_under_test")
core_pkg.__path__ = [str(PROJECT_ROOT / "core")]
sys.modules["core_pkg_under_test"] = core_pkg
sys.modules["core_pkg_under_test.llm"] = llm
components_pkg = ModuleType("core_pkg_under_test.components")
components_pkg.__path__ = [str(PROJECT_ROOT / "core" / "components")]
sys.modules["core_pkg_under_test.components"] = components_pkg
provider_spec = importlib.util.spec_from_file_location(
    "core_pkg_under_test.components.llm_provider",
    PROJECT_ROOT / "core" / "components" / "llm_provider.py",
)
provider_module = importlib.util.module_from_spec(provider_spec)
sys.modules["core_pkg_under_test.components.llm_provider"] = provider_module
provider_spec.loader.exec_module(provider_module)


LLMProvider = provider_module.LLMProvider
HEURIST_BACKEND = provider_module.HEURIST_BACKEND
LITELLM_BACKEND = provider_module.LITELLM_BACKEND


# ---------------------------------------------------------------------------
# Mocked litellm.completion / litellm.acompletion responses
# ---------------------------------------------------------------------------


def _completion_response(content: str, tool_calls=None) -> SimpleNamespace:
    message = SimpleNamespace(content=content, tool_calls=tool_calls)
    choice = SimpleNamespace(message=message)
    return SimpleNamespace(choices=[choice])


# ---------------------------------------------------------------------------
# core.llm: low-level LiteLLM call functions
# ---------------------------------------------------------------------------


class TestLitellmKwargs(unittest.TestCase):
    def test_drop_params_default(self):
        kwargs = llm._litellm_kwargs(None, None, 3, None)
        self.assertIs(kwargs["drop_params"], True)
        self.assertEqual(kwargs["num_retries"], 3)

    def test_credentials_passed_when_set(self):
        kwargs = llm._litellm_kwargs("sk", "https://x", 0, None)
        self.assertEqual(kwargs["api_key"], "sk")
        self.assertEqual(kwargs["api_base"], "https://x")

    def test_user_kwargs_override_defaults(self):
        kwargs = llm._litellm_kwargs(None, None, 3, {"drop_params": False, "num_retries": 7})
        self.assertIs(kwargs["drop_params"], False)
        self.assertEqual(kwargs["num_retries"], 7)


class TestCallLlmLitellm(unittest.TestCase):
    def test_returns_content_dict(self):
        with patch("litellm.completion", return_value=_completion_response("4")):
            out = llm.call_llm_litellm(
                base_url=None,
                api_key=None,
                model_id="anthropic/claude-3-5-sonnet-20241022",
                system_prompt="sys",
                user_prompt="What is 2+2?",
            )
        self.assertEqual(out, {"content": "4"})

    def test_propagates_tool_calls(self):
        tool_call = SimpleNamespace(function=SimpleNamespace(name="get_weather", arguments='{"city":"Tokyo"}'))
        with patch(
            "litellm.completion",
            return_value=_completion_response("", tool_calls=[tool_call]),
        ):
            out = llm.call_llm_with_tools_litellm(
                base_url=None,
                api_key=None,
                model_id="anthropic/claude-3-5-sonnet-20241022",
                system_prompt="sys",
                user_prompt="weather?",
                tools=[{"type": "function", "function": {"name": "get_weather"}}],
            )
        self.assertIn("tool_calls", out)

    def test_raises_llmerror_on_failure(self):
        with patch("litellm.completion", side_effect=RuntimeError("net dead")):
            with self.assertRaisesRegex(llm.LLMError, "LiteLLM API call failed"):
                llm.call_llm_litellm(
                    base_url=None,
                    api_key=None,
                    model_id="openai/gpt-4o",
                    system_prompt="x",
                    user_prompt="y",
                )

    def test_passes_temperature_and_max_tokens(self):
        captured = {}

        def fake_completion(**kwargs):
            captured.update(kwargs)
            return _completion_response("ok")

        with patch("litellm.completion", side_effect=fake_completion):
            llm.call_llm_litellm(
                base_url=None,
                api_key=None,
                model_id="openai/gpt-4o",
                system_prompt="s",
                user_prompt="u",
                temperature=0.0,
                max_tokens=64,
                litellm_kwargs={"num_retries": 2},
            )
        self.assertEqual(captured["temperature"], 0.0)
        self.assertEqual(captured["max_tokens"], 64)
        self.assertEqual(captured["num_retries"], 2)
        self.assertIs(captured["drop_params"], True)


class TestCallLlmLitellmAsync(unittest.TestCase):
    def test_async_returns_string(self):
        async def run():
            with patch("litellm.acompletion", return_value=_completion_response("hi")):
                return await llm.call_llm_litellm_async(
                    base_url=None,
                    api_key=None,
                    model_id="openai/gpt-4o",
                    system_prompt="s",
                    user_prompt="u",
                )

        out = asyncio.run(run())
        self.assertEqual(out, "hi")

    def test_async_with_tools_returns_dict(self):
        tool_call = SimpleNamespace(function=SimpleNamespace(name="t", arguments="{}"))

        async def run():
            with patch(
                "litellm.acompletion",
                return_value=_completion_response("", tool_calls=[tool_call]),
            ):
                return await llm.call_llm_with_tools_litellm_async(
                    base_url=None,
                    api_key=None,
                    model_id="openai/gpt-4o",
                    system_prompt="s",
                    user_prompt="u",
                    tools=[{"type": "function", "function": {"name": "t"}}],
                )

        out = asyncio.run(run())
        self.assertIn("tool_calls", out)


# ---------------------------------------------------------------------------
# LLMProvider: backend switch + dispatch
# ---------------------------------------------------------------------------


class TestProviderInit(unittest.TestCase):
    def setUp(self):
        # Make sure HEURIST_* env vars exist so the heurist branch
        # has something to read; tests don't actually call out.
        self._saved = (
            os.environ.get("HEURIST_BASE_URL"),
            os.environ.get("HEURIST_API_KEY"),
        )
        os.environ["HEURIST_BASE_URL"] = "http://example.invalid"
        os.environ["HEURIST_API_KEY"] = "k"

    def tearDown(self):
        base, key = self._saved
        if base is None:
            os.environ.pop("HEURIST_BASE_URL", None)
        else:
            os.environ["HEURIST_BASE_URL"] = base
        if key is None:
            os.environ.pop("HEURIST_API_KEY", None)
        else:
            os.environ["HEURIST_API_KEY"] = key

    def test_default_backend_is_heurist(self):
        p = LLMProvider()
        self.assertEqual(p.provider, HEURIST_BACKEND)
        self.assertEqual(p.base_url, "http://example.invalid")
        self.assertEqual(p.api_key, "k")

    def test_litellm_backend_does_not_pull_heurist_env(self):
        p = LLMProvider(
            provider=LITELLM_BACKEND,
            large_model_id="anthropic/claude-3-5-sonnet-20241022",
        )
        self.assertEqual(p.provider, LITELLM_BACKEND)
        self.assertIsNone(p.base_url)
        self.assertIsNone(p.api_key)

    def test_litellm_backend_accepts_explicit_credentials(self):
        p = LLMProvider(
            provider=LITELLM_BACKEND,
            base_url="https://foundry/anthropic",
            api_key="sk-ant-foundry",
            large_model_id="anthropic/claude-sonnet-4-6",
        )
        self.assertEqual(p.base_url, "https://foundry/anthropic")
        self.assertEqual(p.api_key, "sk-ant-foundry")

    def test_unknown_backend_raises(self):
        with self.assertRaisesRegex(ValueError, "Unknown LLM provider backend"):
            LLMProvider(provider="bogus")


class TestProviderDispatch(unittest.TestCase):
    def test_heurist_dispatch_targets_openai_path(self):
        os.environ["HEURIST_BASE_URL"] = "http://example.invalid"
        os.environ["HEURIST_API_KEY"] = "k"
        p = LLMProvider(large_model_id="some-heurist-model")
        tools_fn, no_tools_fn, extra = p._dispatch()
        self.assertEqual(tools_fn, llm.call_llm_with_tools)
        self.assertEqual(no_tools_fn, llm.call_llm)
        self.assertEqual(extra, {})

    def test_litellm_dispatch_targets_litellm_path(self):
        p = LLMProvider(
            provider=LITELLM_BACKEND,
            large_model_id="anthropic/claude-3-5-sonnet-20241022",
            litellm_kwargs={"num_retries": 5},
        )
        tools_fn, no_tools_fn, extra = p._dispatch()
        self.assertEqual(tools_fn, llm.call_llm_with_tools_litellm)
        self.assertEqual(no_tools_fn, llm.call_llm_litellm)
        self.assertEqual(extra, {"litellm_kwargs": {"num_retries": 5}})

    def test_litellm_dispatch_omits_extra_when_no_kwargs(self):
        p = LLMProvider(
            provider=LITELLM_BACKEND,
            large_model_id="openai/gpt-4o",
        )
        _, _, extra = p._dispatch()
        self.assertEqual(extra, {})


class TestProviderCall(unittest.TestCase):
    def test_litellm_call_routes_through_litellm_completion(self):
        async def run():
            p = LLMProvider(
                provider=LITELLM_BACKEND,
                large_model_id="anthropic/claude-3-5-sonnet-20241022",
            )
            captured = {}

            def fake(**kwargs):
                captured.update(kwargs)
                return _completion_response("4")

            with patch("litellm.completion", side_effect=fake):
                text, image_url, tool_back = await p.call(
                    system_prompt="reply with 4",
                    user_prompt="2+2?",
                    temperature=0.0,
                    max_tokens=32,
                )
            return captured, text, image_url, tool_back

        captured, text, image_url, tool_back = asyncio.run(run())
        self.assertEqual(text, "4")
        self.assertIsNone(image_url)
        self.assertIsNone(tool_back)
        # litellm.completion was indeed called with the litellm-prefixed model
        self.assertEqual(captured["model"], "anthropic/claude-3-5-sonnet-20241022")
        self.assertIs(captured["drop_params"], True)


if __name__ == "__main__":
    unittest.main()
