"""
Benchmark PracticalTools Apify actor for bulk tweet hydration/search.

This script is meant to answer:
- Latency for fetching 5/10/20 tweets by IDs (tweet/by_ids)
- Basic run and dataset metrics (items returned, missing IDs)
- What the returned tweet objects look like (sample prints)

Requires:
- APIFY_API_KEY in env

Optional:
- TWEET_IDS="id1,id2,..." in env (overrides built-in sample IDs)
- Or pass tweet IDs via CLI: --tweet-ids "id1,id2,..." or --tweet-ids-file ./ids.txt

Common commands:
  # Default: batch size 20, 1 run, prints 3 sample items (summary)
  python test_scripts/test_apify_bulk.py

  # Test multiple batch sizes, repeat each size 3 times
  python test_scripts/test_apify_bulk.py --sizes 5 10 20 --runs 3

  # Stress test with a small cooldown between runs + save a JSON report
  python test_scripts/test_apify_bulk.py --sizes 5 10 20 --runs 10 --sleep 2 --out apify_bulk_report.json

  # Print raw returned objects (first item only)
  python test_scripts/test_apify_bulk.py --raw --print 1

  # Provide tweet ids
  python test_scripts/test_apify_bulk.py --tweet-ids "id1,id2,id3,..." --sizes 20
  python test_scripts/test_apify_bulk.py --tweet-ids-file ./tweet_ids.txt --sizes 20
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence, Tuple

from apify_client import ApifyClient
from apify_client._errors import ApifyApiError
from dotenv import load_dotenv

ACTOR_ID = "practicaltools/cheap-simple-twitter-api"

# Load APIFY_API_KEY from repo .env (same pattern used across agents).
load_dotenv()


DEFAULT_TWEET_IDS: List[str] = [
    # Existing repo tests
    "1913624766793289972",
    "1914394032169762877",
    # IDs seen in a public Apify dataset run shared earlier (30 ids)
    "2001257801864372683",
    "2001257758394360259",
    "2001086802581709120",
    "2001086557462429775",
    "2001085514145726480",
    "2001054848935227532",
    "2000977557420646562",
    "2000977141400522823",
    "2000976931764773311",
    "2000976844867121455",
    "2000937762946736303",
    "2000932468720107783",
    "2000930764700213362",
    "2000930543429706196",
    "2000930381797974374",
    "2000921232854962389",
    "2000908837667398095",
    "1999214851835724063",
    "1999081270903734710",
    "1998916235321610319",
    "1998544100191302022",
    "1998372116098580643",
    "1997808981180657807",
    "1996575420758548926",
    "1995986704679784504",
    "1995550083312746968",
    "1995094901051228176",
    "1994301878335885790",
    "1994014931625107727",
    "1994001393515155505",
    # Add more as needed (duplicates are okay for latency tests, but skew results).
]


def _now() -> float:
    return time.perf_counter()


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _chunk(seq: Sequence[str], size: int) -> List[List[str]]:
    return [list(seq[i : i + size]) for i in range(0, len(seq), size)]


def _dedupe_keep_order(ids: Sequence[str]) -> List[str]:
    seen = set()
    out = []
    for x in ids:
        s = str(x).strip()
        if not s or s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


def _load_tweet_ids() -> List[str]:
    raw = os.getenv("TWEET_IDS", "").strip()
    if not raw:
        return DEFAULT_TWEET_IDS
    return _dedupe_keep_order([x.strip() for x in raw.split(",") if x.strip()])


def _load_tweet_ids_from_file(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # allow commas, spaces, and newlines
    raw = content.replace("\n", ",").replace(" ", ",")
    return _dedupe_keep_order([x.strip() for x in raw.split(",") if x.strip()])


@dataclass(frozen=True)
class CallMetrics:
    batch_size: int
    run_index: int
    input_ids: int
    returned_items: int
    missing_ids: int
    actor_call_s: float
    dataset_read_s: float
    total_s: float
    run_id: Optional[str] = None
    dataset_id: Optional[str] = None
    error: Optional[str] = None


def _call_practicaltools_by_ids(
    client: ApifyClient, tweet_ids: List[str], *, chunk_size: int = 20
) -> Tuple[List[Dict[str, Any]], List[str], Dict[str, Any]]:
    ids = _dedupe_keep_order(tweet_ids)
    if not ids:
        return [], [], {"error": "No tweet IDs provided"}

    all_items: List[Dict[str, Any]] = []
    for part in _chunk(ids, chunk_size):
        run_input = {"endpoint": "tweet/by_ids", "parameters": {"tweet_ids": ",".join(part)}}
        run = client.actor(ACTOR_ID).call(run_input=run_input)
        dataset_id = run.get("defaultDatasetId")
        if not dataset_id:
            return [], ids, {"error": "Actor run returned no dataset id", "run": run}
        items = list(client.dataset(dataset_id).iterate_items())
        all_items.extend([it for it in items if isinstance(it, dict)])

    returned_ids = {str(it.get("id")) for it in all_items if it.get("id")}
    missing = [tid for tid in ids if tid not in returned_ids]
    return all_items, missing, {"status": "success"}


def _simplify_tweet(item: Dict[str, Any]) -> Dict[str, Any]:
    author = (item.get("author") or {}) if isinstance(item.get("author"), dict) else {}
    return {
        "id": str(item.get("id") or ""),
        "text": item.get("text") or item.get("fullText") or "",
        "createdAt": item.get("createdAt"),
        "url": item.get("url") or item.get("twitterUrl"),
        "lang": item.get("lang"),
        "isReply": item.get("isReply"),
        "isRetweet": item.get("isRetweet"),
        "isQuote": item.get("isQuote"),
        "retweetCount": item.get("retweetCount"),
        "replyCount": item.get("replyCount"),
        "likeCount": item.get("likeCount"),
        "quoteCount": item.get("quoteCount"),
        "bookmarkCount": item.get("bookmarkCount"),
        "viewCount": item.get("viewCount"),
        "author": {
            "id": str(author.get("id") or ""),
            "userName": author.get("userName"),
            "name": author.get("name"),
            "followers": author.get("followers"),
            "isVerified": author.get("isVerified"),
            "isBlueVerified": author.get("isBlueVerified"),
        },
    }


def _single_run(
    client: ApifyClient, tweet_ids: List[str], *, batch_size: int, run_index: int
) -> Tuple[CallMetrics, List[Dict[str, Any]]]:
    # For a clean latency test, we only use the first N ids.
    ids = _dedupe_keep_order(tweet_ids)[:batch_size]

    t0 = _now()
    # actor call + dataset read is encapsulated inside helper, but we split timers by re-running call inline:
    run_input = {"endpoint": "tweet/by_ids", "parameters": {"tweet_ids": ",".join(ids)}}
    t1 = _now()
    run: Dict[str, Any] = {}
    dataset_id: Optional[str] = None
    items: List[Dict[str, Any]] = []
    error: Optional[str] = None
    try:
        run = client.actor(ACTOR_ID).call(run_input=run_input)
        t2 = _now()
        dataset_id = run.get("defaultDatasetId")
        if dataset_id:
            items = list(client.dataset(dataset_id).iterate_items())
        t3 = _now()
    except ApifyApiError as e:
        t2 = _now()
        t3 = t2
        error = str(e)
    except Exception as e:
        t2 = _now()
        t3 = t2
        error = str(e)

    returned_ids = {str(it.get("id")) for it in items if isinstance(it, dict) and it.get("id")}
    missing = [tid for tid in ids if tid not in returned_ids]

    metrics = CallMetrics(
        batch_size=batch_size,
        run_index=run_index,
        input_ids=len(ids),
        returned_items=len(items),
        missing_ids=len(missing),
        actor_call_s=(t2 - t1),
        dataset_read_s=(t3 - t2),
        total_s=(t3 - t0),
        run_id=run.get("id"),
        dataset_id=dataset_id,
        error=error,
    )
    return metrics, items


def _summarize(metrics: List[CallMetrics]) -> Dict[str, Any]:
    def s(vals: List[float]) -> Dict[str, float]:
        if not vals:
            return {"min": 0.0, "avg": 0.0, "p50": 0.0, "max": 0.0}
        return {
            "min": min(vals),
            "avg": sum(vals) / len(vals),
            "p50": statistics.median(vals),
            "max": max(vals),
        }

    return {
        "runs": len(metrics),
        "errors": sum(1 for m in metrics if m.error),
        "actor_call_s": s([m.actor_call_s for m in metrics]),
        "dataset_read_s": s([m.dataset_read_s for m in metrics]),
        "total_s": s([m.total_s for m in metrics]),
        "returned_items": {
            "min": min((m.returned_items for m in metrics), default=0),
            "avg": sum((m.returned_items for m in metrics), 0) / max(len(metrics), 1),
            "max": max((m.returned_items for m in metrics), default=0),
        },
        "missing_ids": {
            "min": min((m.missing_ids for m in metrics), default=0),
            "avg": sum((m.missing_ids for m in metrics), 0) / max(len(metrics), 1),
            "max": max((m.missing_ids for m in metrics), default=0),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark Apify PracticalTools tweet/by_ids latency")
    parser.add_argument("--batch-sizes", "--sizes", "-s", nargs="+", type=int, default=[20], dest="batch_sizes")
    parser.add_argument("--runs-per-size", "--runs", "-r", type=int, default=1, dest="runs_per_size")
    parser.add_argument("--sleep-between", "--sleep", type=float, default=0.0, dest="sleep_between")
    parser.add_argument(
        "--print-items",
        "--print",
        "-p",
        type=int,
        default=3,
        help="Print up to N returned items per run (0 disables).",
        dest="print_items",
    )
    parser.add_argument(
        "--print-mode",
        choices=["raw", "summary"],
        default="summary",
        help="raw prints full dicts; summary prints a compact view.",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Shortcut for --print-mode raw",
    )
    parser.add_argument(
        "--dump-json",
        "--out",
        type=str,
        default="",
        help="Write all run metrics + printed items to a JSON file for offline analysis.",
        dest="dump_json",
    )
    parser.add_argument(
        "--tweet-ids",
        type=str,
        default="",
        help="Comma-separated tweet IDs (overrides env/default list).",
    )
    parser.add_argument(
        "--tweet-ids-file",
        type=str,
        default="",
        help="Path to a file containing tweet IDs (comma/space/newline separated). Overrides env/default list.",
    )
    args = parser.parse_args()

    if args.raw:
        args.print_mode = "raw"

    api_key = os.getenv("APIFY_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("APIFY_API_KEY is required")

    if args.tweet_ids_file:
        tweet_ids = _load_tweet_ids_from_file(args.tweet_ids_file)
    elif args.tweet_ids:
        tweet_ids = _dedupe_keep_order([x.strip() for x in args.tweet_ids.split(",") if x.strip()])
    else:
        tweet_ids = _load_tweet_ids()

    if len(tweet_ids) < max(args.batch_sizes):
        raise SystemExit(
            f"Need at least {max(args.batch_sizes)} tweet IDs (got {len(tweet_ids)}). "
            f"Set TWEET_IDS env var to provide more."
        )

    client = ApifyClient(api_key)
    started_iso = _utc_now_iso()
    print(f"Actor: {ACTOR_ID}")
    print(f"Total tweet IDs available: {len(tweet_ids)}")
    print(f"Batch sizes: {args.batch_sizes} | Runs per size: {args.runs_per_size}\n")
    print(f"Started (UTC): {started_iso}\n")

    all_metrics: List[CallMetrics] = []
    dump: Dict[str, Any] = {
        "actor": ACTOR_ID,
        "started_utc": started_iso,
        "batch_sizes": args.batch_sizes,
        "runs_per_size": args.runs_per_size,
        "print_items": args.print_items,
        "print_mode": args.print_mode,
        "runs": [],
    }
    for batch_size in args.batch_sizes:
        group: List[CallMetrics] = []
        for i in range(args.runs_per_size):
            run_started_iso = _utc_now_iso()
            m, items = _single_run(client, tweet_ids, batch_size=batch_size, run_index=i + 1)
            run_finished_iso = _utc_now_iso()
            group.append(m)
            all_metrics.append(m)
            if m.error:
                print(
                    f"[batch={batch_size:>2}] run {i + 1}/{args.runs_per_size} ERROR: {m.error} "
                    f"(actor_call={m.actor_call_s:.2f}s)"
                )
            else:
                print(
                    f"[batch={batch_size:>2}] run {i + 1}/{args.runs_per_size} "
                    f"actor={m.actor_call_s:.2f}s dataset={m.dataset_read_s:.2f}s total={m.total_s:.2f}s "
                    f"returned={m.returned_items} missing={m.missing_ids} "
                    f"runId={m.run_id} datasetId={m.dataset_id}"
                )
                print(f"  - Run window (UTC): {run_started_iso} -> {run_finished_iso}")
                if m.run_id:
                    print(f"  - Run URL: https://console.apify.com/view/runs/{m.run_id}")
                if m.dataset_id:
                    print(f"  - Dataset URL: https://console.apify.com/storage/datasets/{m.dataset_id}")

                if args.print_items and items:
                    n = min(args.print_items, len(items))
                    sample = items[:n]
                    if args.print_mode == "raw":
                        print(f"  - Sample items (raw, first {n}):")
                        print(json.dumps(sample, ensure_ascii=False, indent=2)[:20000])
                    else:
                        print(f"  - Sample items (summary, first {n}):")
                        summary = [_simplify_tweet(x) for x in sample if isinstance(x, dict)]
                        print(json.dumps(summary, ensure_ascii=False, indent=2)[:20000])

                dump["runs"].append(
                    {
                        "run_started_utc": run_started_iso,
                        "run_finished_utc": run_finished_iso,
                        "metrics": asdict(m),
                        "sample_items": (
                            items[: min(args.print_items, len(items))]
                            if (not m.error and args.print_items and items)
                            else []
                        ),
                    }
                )
            if args.sleep_between and (i + 1) < args.runs_per_size:
                time.sleep(args.sleep_between)

        summary = _summarize(group)
        print(f"\nSummary for batch={batch_size}: {summary}\n")

    print("Raw metrics (for copy/paste):")
    print([asdict(m) for m in all_metrics])

    finished_iso = _utc_now_iso()
    dump["finished_utc"] = finished_iso
    if args.dump_json:
        with open(args.dump_json, "w", encoding="utf-8") as f:
            json.dump(dump, f, ensure_ascii=False, indent=2)
        print(f"\nWrote JSON report: {args.dump_json}")
    print(f"\nFinished (UTC): {finished_iso}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
