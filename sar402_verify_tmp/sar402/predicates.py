# --- PROVENANCE (do not remove) --------------------------------------------
# canonical source repository : SAR-402 reference implementation
# exact source commit SHA     : 73bc7529929fdc00e0fdf09f5463338e34fc519d
# original source file path   : sar402_reference/sar402/predicates.py
# date copied                 : 2026-07-31
# scope                       : verification-only Heurist adapter support
# status                      : NON-CANONICAL TEMPORARY COPY
# Canonical logic remains in the SAR-402 reference implementation at the path/commit above. Shared-core
# packaging was deferred pending actual Heurist interest or review -- this is
# a disposable local copy, not a package release. Future maintenance MUST
# diff this file against the recorded reference-implementation source commit before
# modification or any submission.
# -----------------------------------------------------------------------------
"""Pure local evaluators for the canonical five Continuity predicates.

Each evaluator takes normalized `SettlementEvidence` and returns exactly one of
PASS | FAIL | INDETERMINATE. There is no second verdict vocabulary and there are
no x402-specific predicates. Insufficient evidence yields INDETERMINATE; it is
never guessed.

Semantic mapping (from the SAR-402 profile, §15):

    object_continuity     paid resource/action matches delivered resource/action
    constraint_continuity quote vs settlement: amount, asset, chain, recipient, quote id
    temporal_continuity   payment/delivery within the authorized quote window
    authority_continuity  payer/agent/wallet authorized for the settlement context
    executor_continuity    resource/action actually delivered; pre-delivery => INDETERMINATE
"""

from __future__ import annotations

from typing import Dict

from .constants import (
    FAIL,
    INDETERMINATE,
    PASS,
    PRE_DELIVERY_POINTS,
)
from .models import SettlementEvidence, parse_timestamp


def object_continuity(ev: SettlementEvidence) -> str:
    """Paid for resource A, received resource A — not resource B."""
    if not ev.resource:
        return INDETERMINATE
    if ev.delivery is None:
        # Pre-delivery: the object identity is preserved up to settlement
        # (the payment references the quoted resource). Delivery is evaluated
        # by executor_continuity once it exists.
        return PASS
    delivered = ev.delivery.delivered_resource
    if not delivered:
        return INDETERMINATE
    return PASS if delivered == ev.resource else FAIL


def constraint_continuity(ev: SettlementEvidence) -> str:
    """Price, asset, recipient, chain, and quote id did not drift between the
    402 challenge and settlement."""
    if not ev.quote_id:
        return INDETERMINATE
    if ev.price is None:
        return INDETERMINATE
    paid = ev.effective_amount_paid
    checks = (
        ev.price.amount == paid.amount,
        ev.price.decimals == paid.decimals,
        ev.asset == paid.asset,
        ev.asset == ev.effective_settled_asset,
        ev.chain == ev.effective_settled_chain,
        ev.recipient == ev.effective_settled_recipient,
    )
    return PASS if all(checks) else FAIL


def temporal_continuity(ev: SettlementEvidence) -> str:
    """Settlement and delivery occurred inside the valid quote/payment window."""
    window_end = parse_timestamp(ev.quote_expires_at)
    if window_end is None:
        return INDETERMINATE
    window_start = parse_timestamp(ev.quoted_at)

    observed = []
    for ts in (ev.paid_at, ev.delivered_at):
        parsed = parse_timestamp(ts)
        if parsed is not None:
            observed.append(parsed)
    if not observed:
        return INDETERMINATE

    for moment in observed:
        if moment > window_end:
            return FAIL
        if window_start is not None and moment < window_start:
            return FAIL
    return PASS


def authority_continuity(ev: SettlementEvidence) -> str:
    """The paying wallet / delegated agent was permitted to settle and receive."""
    if ev.authorized_payers is None:
        return INDETERMINATE
    if not ev.payer:
        return INDETERMINATE
    allowed = {a.lower() for a in ev.authorized_payers}
    candidates = {ev.payer.lower()}
    if ev.agent:
        candidates.add(ev.agent.lower())
    if ev.wallet:
        candidates.add(ev.wallet.lower())
    return PASS if candidates & allowed else FAIL


def executor_continuity(ev: SettlementEvidence) -> str:
    """The resource server actually performed the authorized delivery.

    Pre-delivery (no delivery evidence) is INDETERMINATE: it is not yet
    knowable, not a failure."""
    if ev.delivery is None:
        return INDETERMINATE
    if ev.delivery.failed:
        return FAIL
    delivered = ev.delivery.delivered_resource
    if not delivered:
        return INDETERMINATE
    return PASS if delivered == ev.resource else FAIL


_EVALUATORS = {
    "object_continuity": object_continuity,
    "constraint_continuity": constraint_continuity,
    "temporal_continuity": temporal_continuity,
    "authority_continuity": authority_continuity,
    "executor_continuity": executor_continuity,
}


def evaluate_continuity(ev: SettlementEvidence) -> Dict[str, str]:
    """Evaluate all five predicates. Returns a dict in canonical predicate order."""
    return {name: fn(ev) for name, fn in _EVALUATORS.items()}


def derive_verdict(continuity: Dict[str, str], verification_point: str) -> str:
    """Aggregate the five predicates into a single sar_verdict.

    Rules:
      * Any FAIL  -> FAIL.
      * Otherwise, executor_continuity == INDETERMINATE is *expected* at
        pre-delivery seams and is not, by itself, verdict-blocking (this is why
        a gate-mode payment_verified_pre_delivery receipt can be PASS while
        executor_continuity is INDETERMINATE).
      * Any remaining INDETERMINATE -> INDETERMINATE.
      * Else PASS.
    """
    values = dict(continuity)
    if any(v == FAIL for v in values.values()):
        return FAIL

    ignorable = set()
    if verification_point in PRE_DELIVERY_POINTS:
        ignorable.add("executor_continuity")

    for name, value in values.items():
        if value == INDETERMINATE and name not in ignorable:
            return INDETERMINATE
    return PASS
