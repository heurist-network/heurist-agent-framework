# --- PROVENANCE (do not remove) --------------------------------------------
# canonical source repository : SAR-402 reference implementation
# exact source commit SHA     : 73bc7529929fdc00e0fdf09f5463338e34fc519d
# original source file path   : sar402_reference/sar402/models.py
# date copied                 : 2026-07-31
# scope                       : verification-only Heurist adapter support
# status                      : NON-CANONICAL TEMPORARY COPY
# Canonical logic remains in the SAR-402 reference implementation at the path/commit above. Shared-core
# packaging was deferred pending actual Heurist interest or review -- this is
# a disposable local copy, not a package release. Future maintenance MUST
# diff this file against the recorded reference-implementation source commit before
# modification or any submission.
# -----------------------------------------------------------------------------
"""Normalized input models for SAR-402.

These are the local, network-free representation of the evidence a future
SAR-402 agent will collect from an x402 flow:

    * the 402 quote / challenge constraints,
    * the verified payment / settlement actuals,
    * optional delivery evidence.

Nothing here parses live x402 payloads or touches a chain. The agent is
expected to normalize its raw evidence into a `SettlementEvidence` and hand it
to the predicate evaluators and the builder.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Sequence


@dataclass(frozen=True)
class Amount:
    """An on-chain amount carried as an integer string with explicit decimals
    to avoid float drift."""

    amount: str
    asset: str
    decimals: int

    def as_dict(self) -> dict:
        return {"amount": self.amount, "asset": self.asset, "decimals": self.decimals}

    def matches(self, other: "Amount") -> bool:
        return (
            self.amount == other.amount
            and self.asset == other.asset
            and self.decimals == other.decimals
        )


@dataclass(frozen=True)
class DeliveryEvidence:
    """Evidence that the resource/action was (or was not) delivered.

    `failed=True` records an attempted-but-failed delivery. Absence of a
    DeliveryEvidence object altogether means delivery has not happened or has
    not been observed (pre-delivery)."""

    delivered_resource: str
    evidence_type: str
    evidence_digest: Optional[str] = None
    status_code: Optional[int] = None
    delivered_at: Optional[str] = None
    failed: bool = False

    def as_dict(self) -> dict:
        out = {
            "delivered_resource": self.delivered_resource,
            "evidence_type": self.evidence_type,
        }
        if self.evidence_digest is not None:
            out["evidence_digest"] = self.evidence_digest
        if self.status_code is not None:
            out["status_code"] = self.status_code
        if self.delivered_at is not None:
            out["delivered_at"] = self.delivered_at
        return out


@dataclass
class SettlementEvidence:
    """Normalized evidence for one x402 settlement.

    Quote-side fields (resource, quote_id, price, asset, chain, recipient)
    describe what the 402 challenge authorized. Settlement-side overrides
    (amount_paid, settled_asset, settled_chain, settled_recipient) describe the
    actuals; when an override is None it is treated as equal to the quote side
    (i.e. no drift). This lets the predicate evaluators detect constraint drift
    without forcing every caller to restate matching values.
    """

    # Quote / authorized constraints
    resource: str
    quote_id: str
    price: Amount
    asset: str
    chain: str  # CAIP-2 style, e.g. "eip155:8453". Chain-agnostic. Not Base-only.
    recipient: str
    payer: str
    payment_ref: str

    # Settlement actuals (default to the quote side when None)
    amount_paid: Optional[Amount] = None
    settled_asset: Optional[str] = None
    settled_chain: Optional[str] = None
    settled_recipient: Optional[str] = None

    # Identity / authority context
    facilitator: Optional[str] = None
    agent: Optional[str] = None
    wallet: Optional[str] = None
    # Wallets/agents authorized for this settlement context. None => unknown
    # (authority_continuity is INDETERMINATE rather than guessed).
    authorized_payers: Optional[Sequence[str]] = None

    # Timestamps (ISO 8601). quoted_at / verified_at / issued_at are required
    # by the schema; the rest are optional context.
    quoted_at: Optional[str] = None
    paid_at: Optional[str] = None
    verified_at: Optional[str] = None
    delivered_at: Optional[str] = None
    issued_at: Optional[str] = None
    quote_expires_at: Optional[str] = None

    # Delivery evidence (None => pre-delivery / not observed)
    delivery: Optional[DeliveryEvidence] = None

    # ---- derived accessors -------------------------------------------------

    @property
    def effective_amount_paid(self) -> Amount:
        return self.amount_paid if self.amount_paid is not None else self.price

    @property
    def effective_settled_asset(self) -> str:
        return self.settled_asset if self.settled_asset is not None else self.asset

    @property
    def effective_settled_chain(self) -> str:
        return self.settled_chain if self.settled_chain is not None else self.chain

    @property
    def effective_settled_recipient(self) -> str:
        return (
            self.settled_recipient
            if self.settled_recipient is not None
            else self.recipient
        )


def parse_timestamp(value: Optional[str]) -> Optional[datetime]:
    """Best-effort ISO-8601 parse. Returns None if value is falsy or unparsable.

    Accepts a trailing 'Z'. Naive datetimes are treated as UTC so that
    comparisons across the evidence are consistent."""

    if not value:
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt
