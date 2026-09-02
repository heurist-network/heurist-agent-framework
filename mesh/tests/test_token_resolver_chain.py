"""Unit tests for TokenResolver chain normalization (no network)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mesh.agents.token_resolver_agent import _normalize_chain  # noqa: E402


def test_normalize_robinhood_aliases():
    assert _normalize_chain("robinhood") == "robinhood"
    assert _normalize_chain("Robinhood") == "robinhood"
    assert _normalize_chain("4663") == "robinhood"
    assert _normalize_chain(4663) == "robinhood"
    assert _normalize_chain("robinhood-chain") == "robinhood"
    assert _normalize_chain("robinhood_chain") == "robinhood"
    assert _normalize_chain("Robinhood Chain") == "robinhood"


def test_normalize_existing_chain_aliases():
    assert _normalize_chain("eth") == "ethereum"
    assert _normalize_chain("base") == "base"
    assert _normalize_chain("binance-smart-chain") == "bsc"
    assert _normalize_chain(None) is None
    assert _normalize_chain("") is None
