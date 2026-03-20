import asyncio
import csv
import html
import logging
import os
import re
import time
import zipfile
from datetime import datetime
from difflib import SequenceMatcher
from html.parser import HTMLParser
from io import TextIOWrapper
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiohttp
from dotenv import load_dotenv

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

load_dotenv()
logger = logging.getLogger(__name__)

SEC_DATA_BASE_URL = "https://data.sec.gov"
SEC_WWW_BASE_URL = "https://www.sec.gov"
SEC_13F_PAGE_URL = "https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets"

DEFAULT_TIMELINE_FORMS = ["8-K", "10-Q", "10-K", "S-1", "S-1/A"]
INSIDER_FORMS = {"3", "4", "5"}
ACTIVIST_FORMS = {"SC 13D", "SC 13D/A", "SC 13G", "SC 13G/A"}
FACT_FREQUENCIES = {"quarterly", "annual", "all"}
FORM_DIFF_CANDIDATES = ["10-Q", "10-K", "8-K", "S-1", "S-1/A"]

TRANSACTION_CODE_LABELS = {
    "P": "open market purchase",
    "S": "open market sale",
    "M": "option exercise",
    "A": "grant or other award",
    "D": "disposition back to issuer",
    "F": "tax withholding or payment",
}

COMMON_METRIC_ALIASES = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"],
    "net income": ["NetIncomeLoss", "ProfitLoss"],
    "operating income": ["OperatingIncomeLoss"],
    "gross profit": ["GrossProfit"],
    "free cash flow": ["FreeCashFlow"],
    "cash": ["CashAndCashEquivalentsAtCarryingValue", "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"],
    "assets": ["Assets"],
    "liabilities": ["Liabilities"],
    "equity": ["StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"],
    "shares outstanding": [
        "EntityCommonStockSharesOutstanding",
        "CommonStocksIncludingAdditionalPaidInCapitalSharesOutstanding",
    ],
    "eps": ["EarningsPerShareDiluted", "EarningsPerShareBasic"],
}

COMPANY_NAME_STOPWORDS = {
    "INC",
    "INCORPORATED",
    "CORP",
    "CORPORATION",
    "CO",
    "COMPANY",
    "LTD",
    "LIMITED",
    "PLC",
    "HOLDING",
    "HOLDINGS",
    "GROUP",
    "NV",
    "SA",
    "SE",
    "AG",
    "LP",
    "LLC",
    "NEW",
}


class FilingTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts: List[str] = []

    def handle_starttag(self, tag: str, attrs):
        if tag in {"br", "p", "div", "tr", "li", "table", "hr"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str):
        if tag in {"p", "div", "tr", "li", "table", "td", "th", "center"}:
            self.parts.append("\n")

    def handle_data(self, data: str):
        text = data.strip()
        if text:
            self.parts.append(text)

    def get_text(self) -> str:
        text = "".join(self.parts)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n[ \t]+", "\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


def _normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def _normalize_company_name(value: str) -> str:
    value = re.sub(r"[^A-Z0-9 ]+", " ", value.upper())
    tokens = [token for token in value.split() if token not in COMPANY_NAME_STOPWORDS]
    return " ".join(tokens)


def _normalize_issuer_name(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^A-Z0-9 ]+", " ", value.upper())).strip()


def _normalize_identifier(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "", value.upper())


def _safe_float(value: str) -> Optional[float]:
    cleaned = value.replace("$", "").replace(",", "").replace("%", "").strip()
    if not cleaned:
        return None
    return float(cleaned)


def _safe_int(value: str) -> Optional[int]:
    cleaned = value.replace(",", "").strip()
    if not cleaned:
        return None
    if "." in cleaned:
        return int(float(cleaned))
    return int(cleaned)


def _pad_cik(cik: str) -> str:
    return str(cik).zfill(10)


def _filing_sort_key(row: Dict[str, Any]) -> str:
    return row["acceptance_datetime"] or row["filing_date"]


def _build_filing_url(cik: str, accession_number: str, primary_document: str) -> str:
    accession_no_dash = accession_number.replace("-", "")
    cik_no_pad = str(int(cik))
    return f"{SEC_WWW_BASE_URL}/Archives/edgar/data/{cik_no_pad}/{accession_no_dash}/{primary_document}"


def _value_or_default(value: Optional[str], default: str = "") -> str:
    if value is None:
        return default
    return value


def _parse_date(value: str) -> Optional[datetime]:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%d-%b-%Y", "%d-%b-%y", "%m/%d/%Y"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def _period_label(observation: Dict[str, Any]) -> str:
    start = observation.get("start")
    end = observation.get("end") or observation.get("filed")
    if start:
        return f"{start} to {end}"
    return end


class SecEdgarAgent(MeshAgent):
    _throttle_lock: Optional[asyncio.Lock] = None
    _last_request_at = 0.0

    def __init__(self):
        super().__init__()
        self.sec_user_agent = os.getenv("SEC_EDGAR_USER_AGENT") or "heurist-agent-framework/1.0 contact@heurist.ai"
        if self.__class__._throttle_lock is None:
            self.__class__._throttle_lock = asyncio.Lock()

        self.metadata.update(
            {
                "name": "SEC Edgar Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Issuer-first SEC EDGAR agent for company resolution, filing timelines, filing diffs, XBRL fact trends, insider activity, activist filings, and 13F institutional holder snapshots.",
                "external_apis": ["SEC EDGAR", "SEC XBRL", "SEC Form 13F Data Sets"],
                "tags": ["Finance", "Regulatory Filings"],
                "verified": True,
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Heurist.png",
                "examples": [
                    "Resolve the SEC CIK for Apple",
                    "Show the latest 8-K, 10-Q, and 10-K filings for Tesla",
                    "What changed since Apple's last 10-Q?",
                    "Give me Apple revenue trend from SEC XBRL facts",
                    "Show recent Tesla insider activity",
                    "Watch activist filings for Apple",
                    "Show institutional holders for Apple from the latest 13F dataset",
                ],
                "credits": {"default": 0.2},
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.002",
                },
            }
        )

    def get_default_timeout_seconds(self) -> Optional[int]:
        return 45

    def get_tool_timeout_seconds(self) -> Dict[str, int]:
        return {"filing_diff": 60, "institutional_holders": 120}

    def get_system_prompt(self) -> str:
        return """You are an SEC EDGAR filings assistant.

Use the tools with narrow scope:
- `resolve_company` when the company, ticker, or CIK is ambiguous
- `filing_timeline` for 8-K, 10-Q, 10-K, S-1, and related filing events
- `filing_diff` when the user asks what changed since the last same-form filing
- `xbrl_fact_trends` for direct SEC-reported metrics from companyfacts JSON
- `insider_activity` for Forms 3, 4, and 5
- `activist_watch` for Schedule 13D and 13G activity
- `institutional_holders` for issuer-level 13F holder snapshots from the latest flattened SEC dataset

Rules:
- Resolve the issuer before citing filings when the user gives a company name instead of a CIK
- Prefer direct SEC facts and filing links over paraphrased vendor-style summaries
- Be explicit when a comparison is paragraph-level or when 13F matching is based on issuer-name matching
- Mention the exact filing form, filing date, and report period when available
"""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "resolve_company",
                    "description": "Resolve a company name, stock ticker, or CIK into a canonical SEC issuer record with CIK, ticker, and company title. Use this before other SEC tools when the issuer is ambiguous.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Company name, ticker, or CIK to resolve.",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of candidate matches to return.",
                                "default": 5,
                            },
                        },
                        "required": ["query"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "filing_timeline",
                    "description": "Return a compact SEC filing timeline for an issuer. Best for 8-K, 10-Q, 10-K, S-1, and nearby filing events.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Company name, ticker, or CIK.",
                            },
                            "forms": {
                                "type": "array",
                                "description": "Optional SEC form filter. Use exact form strings such as '8-K', '10-Q', '10-K', 'S-1', 'S-1/A', '6-K', '20-F', or '424B5'. Omit to use the default issuer-event set ['8-K', '10-Q', '10-K', 'S-1', 'S-1/A'].",
                                "items": {
                                    "type": "string",
                                    "description": "Exact SEC form code such as '8-K' or '10-Q'.",
                                },
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of filing events to return.",
                                "default": 10,
                            },
                        },
                        "required": ["query"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "filing_diff",
                    "description": "Compare the latest filing with the previous filing of the same form and highlight paragraph-level additions, removals, and filing metadata differences. Use this for 'what changed since last filing'.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Company name, ticker, or CIK.",
                            },
                            "form": {
                                "type": "string",
                                "enum": FORM_DIFF_CANDIDATES,
                                "description": "Optional form to compare. If omitted, the latest comparable major form is used.",
                            },
                            "paragraph_limit": {
                                "type": "integer",
                                "description": "Maximum number of added and removed paragraphs to surface.",
                                "default": 5,
                            },
                        },
                        "required": ["query"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "xbrl_fact_trends",
                    "description": "Return direct SEC XBRL company facts for a metric such as revenue, net income, EPS, cash, assets, liabilities, or shares outstanding. Use this instead of vendor-normalized fundamentals when the user wants SEC-reported values.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Company name, ticker, or CIK.",
                            },
                            "metric": {
                                "type": "string",
                                "description": "Single metric only. Use a plain-English metric like 'revenue', 'net income', 'operating income', 'gross profit', 'cash', 'assets', 'liabilities', 'equity', 'shares outstanding', or 'eps', or pass an exact SEC XBRL concept like 'RevenueFromContractWithCustomerExcludingAssessedTax', 'NetIncomeLoss', 'Assets', or 'EntityCommonStockSharesOutstanding'. Do not combine multiple metrics in one string.",
                            },
                            "frequency": {
                                "type": "string",
                                "enum": ["quarterly", "annual", "all"],
                                "description": "Observation frequency filter.",
                                "default": "quarterly",
                            },
                            "taxonomy": {
                                "type": "string",
                                "enum": ["us-gaap", "dei"],
                                "description": "Optional taxonomy filter.",
                            },
                            "unit": {
                                "type": "string",
                                "description": "Optional exact SEC unit key for the selected concept. Common examples include 'USD', 'shares', 'USD/shares', and 'pure', but available units depend on the matched metric. Omit to auto-select the unit with the most observations.",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of observations to return.",
                                "default": 8,
                            },
                        },
                        "required": ["query", "metric"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "insider_activity",
                    "description": "Summarize recent insider activity from SEC Forms 3, 4, and 5 for an issuer, including reporting person names and parsed transaction rows from ownership documents.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Company name, ticker, or CIK.",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of insider filings to inspect.",
                                "default": 5,
                            },
                        },
                        "required": ["query"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "activist_watch",
                    "description": "Summarize recent Schedule 13D and 13G filings for an issuer, including filer names, reported ownership amounts, percent of class, and short text snippets from the filing.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Company name, ticker, or CIK.",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of activist filings to inspect.",
                                "default": 5,
                            },
                        },
                        "required": ["query"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "institutional_holders",
                    "description": "Return an issuer-level holder snapshot from the latest SEC Form 13F flattened dataset. Uses the latest quarterly 13F ZIP, matches the issuer by SEC company name normalization, and aggregates long holder rows by filing manager.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Company name, ticker, or CIK.",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of holder rows to return.",
                                "default": 10,
                            },
                        },
                        "required": ["query"],
                    },
                },
            },
        ]

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        try:
            if tool_name == "resolve_company":
                return await self.resolve_company(function_args["query"], function_args.get("limit", 5))
            if tool_name == "filing_timeline":
                return await self.filing_timeline(
                    function_args["query"], function_args.get("forms"), function_args.get("limit", 10)
                )
            if tool_name == "filing_diff":
                return await self.filing_diff(
                    function_args["query"], function_args.get("form"), function_args.get("paragraph_limit", 5)
                )
            if tool_name == "xbrl_fact_trends":
                return await self.xbrl_fact_trends(
                    query=function_args["query"],
                    metric=function_args["metric"],
                    frequency=function_args.get("frequency", "quarterly"),
                    taxonomy=function_args.get("taxonomy"),
                    unit=function_args.get("unit"),
                    limit=function_args.get("limit", 8),
                )
            if tool_name == "insider_activity":
                return await self.insider_activity(function_args["query"], function_args.get("limit", 5))
            if tool_name == "activist_watch":
                return await self.activist_watch(function_args["query"], function_args.get("limit", 5))
            if tool_name == "institutional_holders":
                return await self.institutional_holders(function_args["query"], function_args.get("limit", 10))
            return {"status": "error", "error": f"Unsupported tool: {tool_name}"}
        except Exception as exc:
            logger.error(f"SEC Edgar tool failure for {tool_name}: {exc}")
            return {"status": "error", "error": str(exc)}

    async def _throttle(self):
        async with self.__class__._throttle_lock:
            now = time.monotonic()
            wait_seconds = 0.25 - (now - self.__class__._last_request_at)
            if wait_seconds > 0:
                await asyncio.sleep(wait_seconds)
            self.__class__._last_request_at = time.monotonic()

    async def _ensure_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def _http_get_json(self, url: str) -> Dict[str, Any]:
        await self._throttle()
        await self._ensure_session()
        headers = {"User-Agent": self.sec_user_agent, "Accept": "application/json"}
        async with self.session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=45)) as response:
            response.raise_for_status()
            return await response.json()

    async def _http_get_text(self, url: str) -> str:
        await self._throttle()
        await self._ensure_session()
        headers = {"User-Agent": self.sec_user_agent}
        async with self.session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=45)) as response:
            response.raise_for_status()
            return await response.text()

    @with_cache(ttl_seconds=86400)
    @with_retry(max_retries=2, delay=1.0)
    async def _fetch_company_tickers(self) -> List[Dict[str, Any]]:
        payload = await self._http_get_json(f"{SEC_WWW_BASE_URL}/files/company_tickers.json")
        records = []
        for row in payload.values():
            records.append(
                {
                    "cik": _pad_cik(str(row["cik_str"])),
                    "ticker": row["ticker"],
                    "title": row["title"],
                }
            )
        return records

    @with_cache(ttl_seconds=1800)
    @with_retry(max_retries=2, delay=1.0)
    async def _fetch_submissions(self, cik: str) -> Dict[str, Any]:
        return await self._http_get_json(f"{SEC_DATA_BASE_URL}/submissions/CIK{_pad_cik(cik)}.json")

    @with_cache(ttl_seconds=1800)
    @with_retry(max_retries=2, delay=1.0)
    async def _fetch_submission_file(self, name: str) -> Dict[str, Any]:
        return await self._http_get_json(f"{SEC_DATA_BASE_URL}/submissions/{name}")

    @with_cache(ttl_seconds=1800)
    @with_retry(max_retries=2, delay=1.0)
    async def _fetch_company_facts(self, cik: str) -> Dict[str, Any]:
        return await self._http_get_json(f"{SEC_DATA_BASE_URL}/api/xbrl/companyfacts/CIK{_pad_cik(cik)}.json")

    @with_cache(ttl_seconds=1800)
    @with_retry(max_retries=2, delay=1.0)
    async def _fetch_filing_text(self, url: str) -> str:
        return await self._http_get_text(url)

    @with_cache(ttl_seconds=21600)
    @with_retry(max_retries=2, delay=1.0)
    async def _resolve_latest_13f_zip_url(self) -> str:
        page = await self._http_get_text(SEC_13F_PAGE_URL)
        matches = re.findall(
            r'href="(/files/structureddata/data/form-13f-data-sets/[^"]+_form13f\.zip)"',
            page,
            flags=re.IGNORECASE,
        )
        if not matches:
            raise ValueError("SEC 13F dataset page did not expose a downloadable ZIP link")
        return f"{SEC_WWW_BASE_URL}{matches[0]}"

    async def _ensure_latest_13f_zip(self) -> Path:
        zip_url = await self._resolve_latest_13f_zip_url()
        path = Path("/tmp") / Path(zip_url).name
        if path.exists():
            return path

        await self._throttle()
        await self._ensure_session()
        headers = {"User-Agent": self.sec_user_agent}
        async with self.session.get(zip_url, headers=headers, timeout=aiohttp.ClientTimeout(total=180)) as response:
            response.raise_for_status()
            with path.open("wb") as handle:
                async for chunk in response.content.iter_chunked(1024 * 256):
                    handle.write(chunk)
        return path

    async def _resolve_company_record(self, query: str) -> Dict[str, Any]:
        result = await self.resolve_company(query, limit=5)
        if result["status"] == "error":
            return result
        return result["data"]["best_match"]

    def _score_company_match(self, query: str, record: Dict[str, Any]) -> float:
        query_norm = _normalize_identifier(query)
        query_name = _normalize_company_name(query)
        ticker_norm = _normalize_identifier(record["ticker"].replace(".", "-"))
        title_norm = _normalize_company_name(record["title"])

        if query_norm == _normalize_identifier(record["cik"]):
            return 100.0
        if query_norm == ticker_norm:
            return 95.0
        if query_name and query_name == title_norm:
            return 92.0
        if ticker_norm.startswith(query_norm) and query_norm:
            return 84.0
        if query_name and title_norm.startswith(query_name):
            return 80.0
        if query_name and query_name in title_norm:
            return 76.0
        ratio = SequenceMatcher(None, query_name or query_norm, title_norm or ticker_norm).ratio()
        return round(ratio * 70, 2)

    def _normalize_company_candidate(self, record: Dict[str, Any], score: float) -> Dict[str, Any]:
        return {
            "cik": record["cik"],
            "ticker": record["ticker"],
            "title": record["title"],
            "score": round(score, 2),
        }

    def _recent_block_to_rows(self, cik: str, block: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        count = len(block["accessionNumber"])
        for index in range(count):
            primary_document = block["primaryDocument"][index]
            accession_number = block["accessionNumber"][index]
            items_text = _value_or_default(block["items"][index]) if "items" in block else ""
            rows.append(
                {
                    "cik": _pad_cik(cik),
                    "accession_number": accession_number,
                    "filing_date": block["filingDate"][index],
                    "report_date": _value_or_default(block["reportDate"][index]),
                    "acceptance_datetime": _value_or_default(block["acceptanceDateTime"][index]),
                    "form": block["form"][index],
                    "file_number": _value_or_default(block["fileNumber"][index]),
                    "items": [item.strip() for item in items_text.split(",") if item.strip()],
                    "primary_document": primary_document,
                    "primary_doc_description": _value_or_default(block["primaryDocDescription"][index]),
                    "filing_url": _build_filing_url(cik, accession_number, primary_document),
                }
            )
        return rows

    async def _collect_filings(
        self, cik: str, forms: Optional[List[str]] = None, limit: int = 50
    ) -> List[Dict[str, Any]]:
        submissions = await self._fetch_submissions(cik)
        rows = self._recent_block_to_rows(cik, submissions["filings"]["recent"])
        if forms:
            rows = [row for row in rows if row["form"] in forms]

        file_pages = submissions["filings"].get("files", [])
        page_index = 0
        while len(rows) < limit and page_index < len(file_pages):
            page = await self._fetch_submission_file(file_pages[page_index]["name"])
            extra_rows = self._recent_block_to_rows(cik, page)
            if forms:
                extra_rows = [row for row in extra_rows if row["form"] in forms]
            rows.extend(extra_rows)
            page_index += 1

        rows.sort(key=_filing_sort_key, reverse=True)
        return rows[:limit]

    def _html_to_text(self, raw_text: str) -> str:
        cleaned = re.sub(r"<script.*?</script>", " ", raw_text, flags=re.IGNORECASE | re.DOTALL)
        cleaned = re.sub(r"<style.*?</style>", " ", cleaned, flags=re.IGNORECASE | re.DOTALL)
        cleaned = re.sub(r"<ix:header.*?</ix:header>", " ", cleaned, flags=re.IGNORECASE | re.DOTALL)
        upper_cleaned = cleaned.upper()
        anchor = upper_cleaned.find("UNITED STATES SECURITIES AND EXCHANGE COMMISSION")
        if anchor > 0:
            cleaned = cleaned[anchor:]
        if "<" not in cleaned and ">" not in cleaned:
            plain = html.unescape(cleaned)
            plain = re.sub(r"[ \t]+", " ", plain)
            plain = re.sub(r"\n{3,}", "\n\n", plain)
            return plain.strip()

        parser = FilingTextExtractor()
        parser.feed(cleaned)
        return parser.get_text()

    def _extract_paragraphs(self, raw_text: str) -> List[str]:
        text = self._html_to_text(raw_text)
        chunks = re.split(r"\n{2,}", text)
        paragraphs = []
        for chunk in chunks:
            paragraph = _normalize_space(chunk)
            if len(paragraph) >= 80:
                paragraphs.append(paragraph)
        return paragraphs

    def _clean_cell(self, value: str) -> str:
        text = re.sub(r"<[^>]+>", " ", value, flags=re.DOTALL)
        return _normalize_space(text)

    def _extract_first_match(self, pattern: str, text: str) -> str:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
        if match is None:
            return ""
        return self._clean_cell(match.group(1))

    def _parse_ownership_form(self, raw_html: str) -> Dict[str, Any]:
        reporter_name = self._extract_first_match(
            r"Name and Address of Reporting Person<sup>\*</sup></span>.*?<a [^>]*>(.*?)</a>",
            raw_html,
        )
        if not reporter_name:
            reporter_name = self._extract_first_match(
                r"NAME OF REPORTING PERSON.*?</P>.*?<P[^>]*>(.*?)</P>",
                raw_html,
            )

        issuer_name = self._extract_first_match(
            r"Issuer Name <b>and</b> Ticker or Trading Symbol\s*</span><br><a [^>]*>(.*?)</a>",
            raw_html,
        )
        ticker = self._extract_first_match(r"\[\s*<span[^>]*>(.*?)</span>\s*\]", raw_html)
        relationship = self._extract_first_match(
            r"Officer \(give title below\)</td>.*?<td[^>]*style=\"color: blue\">(.*?)</td>",
            raw_html,
        )
        if not relationship:
            relationship = self._extract_first_match(r"TYPE OF REPORTING PERSON.*?<P[^>]*>(.*?)</P>", raw_html)

        transactions: List[Dict[str, Any]] = []
        table_match = re.search(
            r"Table I - Non-Derivative Securities.*?<tbody>(.*?)</tbody>",
            raw_html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if table_match:
            rows = re.findall(r"<tr>(.*?)</tr>", table_match.group(1), flags=re.IGNORECASE | re.DOTALL)
            for row_html in rows:
                cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row_html, flags=re.IGNORECASE | re.DOTALL)
                if len(cells) < 10:
                    continue
                title = self._clean_cell(cells[0])
                if title in {"1. Title of Security (Instr. 3)", ""}:
                    continue
                code = self._clean_cell(cells[3])
                code = re.sub(r"[^A-Z]", "", code)
                amount = self._clean_cell(cells[5])
                acquired_disposed = self._clean_cell(cells[6])
                price = self._clean_cell(cells[7])
                owned_after = self._clean_cell(cells[8])
                transaction_date = self._clean_cell(cells[1])
                if not transaction_date and not code:
                    continue
                transactions.append(
                    {
                        "security_title": title,
                        "transaction_date": transaction_date,
                        "transaction_code": code,
                        "transaction_label": TRANSACTION_CODE_LABELS.get(code, ""),
                        "shares": amount,
                        "direction": acquired_disposed,
                        "price_per_share": price,
                        "shares_owned_after": owned_after,
                        "ownership_form": self._clean_cell(cells[9]),
                    }
                )

        return {
            "reporting_person": reporter_name,
            "issuer_name": issuer_name,
            "ticker": ticker,
            "relationship": relationship,
            "transactions": transactions,
        }

    def _parse_activist_filing(self, raw_html: str) -> Dict[str, Any]:
        plain_text = self._html_to_text(raw_html)
        reporter_name_match = re.search(
            r"NAME\s+OF\s+REPORTING\s+PERSON\s+(.*?)\s+CHECK\s+THE\s+APPROPRIATE\s+BOX\s+IF\s+A\s+MEMBER\s+OF\s+A\s+GROUP",
            plain_text,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if reporter_name_match is None:
            reporter_name_match = re.search(
                r"NAMES\s+OF\s+REPORTING\s+PERSONS\s+(.*?)\s+CHECK\s+THE\s+APPROPRIATE\s+BOX\s+IF\s+A\s+MEMBER\s+OF\s+A\s+GROUP",
                plain_text,
                flags=re.IGNORECASE | re.DOTALL,
            )
        reporter_name = _normalize_space(reporter_name_match.group(1)) if reporter_name_match is not None else ""
        reporter_name = re.sub(r"\s+\d+$", "", reporter_name)

        issuer_match = re.search(
            r"\(Amendment\s+No\..*?\)\s+(.*?)\s+\(Name\s+of\s+Issuer\)",
            plain_text,
            flags=re.IGNORECASE | re.DOTALL,
        )
        issuer_name = _normalize_space(issuer_match.group(1)) if issuer_match is not None else ""

        amount_match = re.search(
            r"AGGREGATE\s+AMOUNT\s+BENEFICIALLY\s+OWNED\s+BY\s+EACH\s+REPORTING\s+PERSON\s+(.*?)\s+CHECK\s+BOX?\s+IF\s+THE\s+AGGREGATE",
            plain_text,
            flags=re.IGNORECASE | re.DOTALL,
        )
        amount_owned = _normalize_space(amount_match.group(1)) if amount_match is not None else ""
        amount_value_match = re.search(r"([\d,]+(?:\.\d+)?\s+shares?[A-Za-z ]*)", amount_owned, flags=re.IGNORECASE)
        if amount_value_match is not None:
            amount_owned = _normalize_space(amount_value_match.group(1))

        percent_match = re.search(
            r"PERCENT\s+OF\s+CLASS\s+REPRESENTED\s+BY\s+AMOUNT\s+IN\s+ROW.*?\s+(.*?)\s+TYPE\s+OF\s+REPORTING\s+PERSON",
            plain_text,
            flags=re.IGNORECASE | re.DOTALL,
        )
        percent_owned = _normalize_space(percent_match.group(1)) if percent_match is not None else ""
        percent_value_match = re.search(r"(\d+(?:\.\d+)?%)", percent_owned)
        if percent_value_match is not None:
            percent_owned = percent_value_match.group(1)

        item_summary = ""
        item_match = re.search(r"(Item 4\..*?)(?:Item 5\.|SIGNATURES)", plain_text, flags=re.IGNORECASE | re.DOTALL)
        if item_match is None:
            item_match = re.search(r"(Item 5\..*?)(?:Item 6\.|SIGNATURES)", plain_text, flags=re.IGNORECASE | re.DOTALL)
        if item_match is not None:
            item_summary = _normalize_space(item_match.group(1))
            if len(item_summary) > 500:
                item_summary = f"{item_summary[:500].rstrip()}..."

        return {
            "reporting_person": reporter_name,
            "issuer_name": issuer_name,
            "beneficial_ownership": amount_owned,
            "percent_of_class": percent_owned,
            "item_summary": item_summary,
        }

    def _dedupe_fact_observations(self, observations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        latest_by_period: Dict[str, Dict[str, Any]] = {}
        for observation in observations:
            period_key = "|".join(
                [
                    _value_or_default(observation.get("start")),
                    _value_or_default(observation.get("end")),
                    _value_or_default(observation.get("form")),
                    str(observation.get("fy", "")),
                    _value_or_default(observation.get("fp")),
                    _value_or_default(observation.get("frame")),
                ]
            )
            existing = latest_by_period.get(period_key)
            if existing is None or _value_or_default(observation.get("filed")) > _value_or_default(
                existing.get("filed")
            ):
                latest_by_period[period_key] = observation
        rows = list(latest_by_period.values())
        rows.sort(key=lambda row: row.get("end") or row.get("filed"), reverse=False)
        return rows

    def _filter_fact_frequency(self, observations: List[Dict[str, Any]], frequency: str) -> List[Dict[str, Any]]:
        if frequency == "all":
            return observations
        if frequency == "quarterly":
            filtered = []
            for row in observations:
                start = _parse_date(_value_or_default(row.get("start")))
                end = _parse_date(_value_or_default(row.get("end")))
                if start and end:
                    if (end - start).days <= 120:
                        filtered.append(row)
                    continue
                if row.get("fp") in {"Q1", "Q2", "Q3"} or row.get("form") == "10-Q":
                    filtered.append(row)
            return filtered
        filtered = []
        for row in observations:
            start = _parse_date(_value_or_default(row.get("start")))
            end = _parse_date(_value_or_default(row.get("end")))
            if start and end:
                if (end - start).days >= 300:
                    filtered.append(row)
                continue
            if row.get("fp") == "FY" or row.get("form") == "10-K":
                filtered.append(row)
        return filtered

    def _resolve_fact_concept(
        self, facts: Dict[str, Any], metric: str, taxonomy_filter: Optional[str]
    ) -> Dict[str, Any]:
        metric_norm = _normalize_identifier(metric)
        metric_name_norm = _normalize_company_name(metric)
        alias_targets = COMMON_METRIC_ALIASES.get(metric.lower(), [])

        candidates: List[Dict[str, Any]] = []
        taxonomies = facts["facts"].keys()
        for taxonomy in taxonomies:
            if taxonomy_filter and taxonomy != taxonomy_filter:
                continue
            for concept_name, concept_payload in facts["facts"][taxonomy].items():
                score = 0.0
                concept_norm = _normalize_identifier(concept_name)
                label = concept_payload.get("label") or concept_name
                description = concept_payload.get("description") or ""
                label_norm = _normalize_company_name(label)
                if concept_name in alias_targets:
                    score = 100.0
                elif metric_norm == concept_norm:
                    score = 96.0
                elif metric_name_norm and metric_name_norm == label_norm:
                    score = 92.0
                elif metric_name_norm and metric_name_norm in label_norm:
                    score = 82.0
                else:
                    ratio = SequenceMatcher(None, metric_name_norm or metric_norm, label_norm or concept_norm).ratio()
                    score = round(ratio * 70, 2)
                if score >= 40:
                    candidates.append(
                        {
                            "taxonomy": taxonomy,
                            "concept": concept_name,
                            "label": label,
                            "description": description,
                            "units": list(concept_payload["units"].keys()),
                            "score": score,
                        }
                    )

        if not candidates:
            return {"status": "error", "error": f"No SEC XBRL metric matched '{metric}'"}

        candidates.sort(key=lambda row: row["score"], reverse=True)
        best = candidates[0]
        concept_payload = facts["facts"][best["taxonomy"]][best["concept"]]
        return {"status": "success", "best": best, "concept_payload": concept_payload, "candidates": candidates[:5]}

    def _select_fact_unit(self, concept_payload: Dict[str, Any], requested_unit: Optional[str]) -> str:
        if requested_unit:
            if requested_unit not in concept_payload["units"]:
                raise ValueError(f"Unit '{requested_unit}' is not available for this concept")
            return requested_unit

        unit_names = list(concept_payload["units"].keys())
        unit_names.sort(key=lambda name: len(concept_payload["units"][name]), reverse=True)
        return unit_names[0]

    def _compact_observation(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "start": observation.get("start"),
            "end": observation.get("end"),
            "filed": observation.get("filed"),
            "form": observation.get("form"),
            "fy": observation.get("fy"),
            "fp": observation.get("fp"),
            "frame": observation.get("frame"),
            "value": observation.get("val"),
            "accession_number": observation.get("accn"),
        }

    def _build_fact_summary(self, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        latest = rows[-1]
        previous = rows[-2] if len(rows) > 1 else None
        summary = {
            "latest_period": _period_label(latest),
            "latest_value": latest["val"],
            "latest_filed": latest.get("filed"),
        }
        if previous is not None:
            delta = latest["val"] - previous["val"]
            summary["previous_period"] = _period_label(previous)
            summary["previous_value"] = previous["val"]
            summary["absolute_change"] = delta
            if previous["val"] not in {0, 0.0}:
                summary["percent_change"] = round((delta / previous["val"]) * 100, 2)
        return summary

    def _parse_13f_tsv_map(self, archive: zipfile.ZipFile, filename: str) -> Dict[str, Dict[str, str]]:
        records: Dict[str, Dict[str, str]] = {}
        with archive.open(filename) as raw:
            reader = csv.DictReader(TextIOWrapper(raw, encoding="utf-8"), delimiter="\t")
            for row in reader:
                records[row["ACCESSION_NUMBER"]] = row
        return records

    async def resolve_company(self, query: str, limit: int = 5) -> Dict[str, Any]:
        query = query.strip()
        if not query:
            return {"status": "error", "error": "query is required"}

        records = await self._fetch_company_tickers()
        scored = []
        for record in records:
            score = self._score_company_match(query, record)
            if score >= 40:
                scored.append(self._normalize_company_candidate(record, score))

        scored.sort(key=lambda row: row["score"], reverse=True)
        if not scored:
            if query.isdigit():
                submissions = await self._fetch_submissions(query)
                best = {
                    "cik": _pad_cik(query),
                    "ticker": submissions["tickers"][0] if submissions["tickers"] else "",
                    "title": submissions["name"],
                    "score": 100.0,
                }
                return {"status": "success", "data": {"query": query, "best_match": best, "candidates": [best]}}
            return {"status": "error", "error": f"No SEC issuer matched '{query}'"}

        limited = scored[: max(limit, 1)]
        return {
            "status": "success",
            "data": {
                "query": query,
                "best_match": limited[0],
                "candidates": limited,
            },
        }

    async def filing_timeline(self, query: str, forms: Optional[List[str]], limit: int) -> Dict[str, Any]:
        company = await self._resolve_company_record(query)
        if "status" in company and company["status"] == "error":
            return company

        form_filter = forms or DEFAULT_TIMELINE_FORMS
        filings = await self._collect_filings(company["cik"], forms=form_filter, limit=max(limit, 10))
        if not filings:
            return {"status": "error", "error": f"No filings found for {company['title']} with forms {form_filter}"}

        counts: Dict[str, int] = {}
        for filing in filings:
            counts[filing["form"]] = counts.get(filing["form"], 0) + 1

        return {
            "status": "success",
            "data": {
                "company": company,
                "forms": form_filter,
                "counts_by_form": counts,
                "filings": filings[:limit],
            },
        }

    async def filing_diff(self, query: str, form: Optional[str], paragraph_limit: int) -> Dict[str, Any]:
        company = await self._resolve_company_record(query)
        if "status" in company and company["status"] == "error":
            return company

        target_forms = [form] if form else FORM_DIFF_CANDIDATES
        filings = await self._collect_filings(company["cik"], forms=target_forms, limit=12)
        if len(filings) < 2:
            return {"status": "error", "error": f"Not enough filings to compare for {company['title']}"}

        if form:
            comparable = [filing for filing in filings if filing["form"] == form]
        else:
            comparable = filings

        if len(comparable) < 2:
            return {"status": "error", "error": f"Could not find two comparable filings for {company['title']}"}

        current_filing = comparable[0]
        previous_filing = comparable[1]

        current_text = await self._fetch_filing_text(current_filing["filing_url"])
        previous_text = await self._fetch_filing_text(previous_filing["filing_url"])

        current_paragraphs = self._extract_paragraphs(current_text)
        previous_paragraphs = self._extract_paragraphs(previous_text)
        current_set = set(current_paragraphs)
        previous_set = set(previous_paragraphs)

        added = [paragraph for paragraph in current_paragraphs if paragraph not in previous_set][:paragraph_limit]
        removed = [paragraph for paragraph in previous_paragraphs if paragraph not in current_set][:paragraph_limit]

        similarity = round(
            SequenceMatcher(None, "\n".join(current_paragraphs), "\n".join(previous_paragraphs)).ratio(),
            4,
        )

        current_items = current_filing["items"]
        previous_items = previous_filing["items"]
        new_items = [item for item in current_items if item not in previous_items]

        return {
            "status": "success",
            "data": {
                "company": company,
                "form": current_filing["form"],
                "comparison_method": "paragraph-level text comparison of the latest filing body versus the previous same-form filing body",
                "current_filing": current_filing,
                "previous_filing": previous_filing,
                "similarity_ratio": similarity,
                "current_paragraph_count": len(current_paragraphs),
                "previous_paragraph_count": len(previous_paragraphs),
                "current_items": current_items,
                "previous_items": previous_items,
                "new_8k_items": new_items,
                "notable_additions": added,
                "notable_removals": removed,
            },
        }

    async def xbrl_fact_trends(
        self,
        query: str,
        metric: str,
        frequency: str = "quarterly",
        taxonomy: Optional[str] = None,
        unit: Optional[str] = None,
        limit: int = 8,
    ) -> Dict[str, Any]:
        if frequency not in FACT_FREQUENCIES:
            return {"status": "error", "error": f"Unsupported frequency: {frequency}"}

        company = await self._resolve_company_record(query)
        if "status" in company and company["status"] == "error":
            return company

        facts = await self._fetch_company_facts(company["cik"])
        concept_result = self._resolve_fact_concept(facts, metric, taxonomy)
        if concept_result["status"] == "error":
            return concept_result

        concept_payload = concept_result["concept_payload"]
        selected_unit = self._select_fact_unit(concept_payload, unit)
        observations = concept_payload["units"][selected_unit]
        observations = self._dedupe_fact_observations(observations)
        observations = self._filter_fact_frequency(observations, frequency)
        if not observations:
            return {
                "status": "error",
                "error": f"No {frequency} SEC XBRL observations matched '{metric}' for {company['title']}",
            }

        trimmed = observations[-limit:]
        return {
            "status": "success",
            "data": {
                "company": company,
                "metric_query": metric,
                "metric": concept_result["best"],
                "candidate_metrics": concept_result["candidates"],
                "frequency": frequency,
                "unit": selected_unit,
                "summary": self._build_fact_summary(trimmed),
                "observations": [self._compact_observation(row) for row in trimmed],
            },
        }

    async def insider_activity(self, query: str, limit: int) -> Dict[str, Any]:
        company = await self._resolve_company_record(query)
        if "status" in company and company["status"] == "error":
            return company

        filings = await self._collect_filings(company["cik"], forms=list(INSIDER_FORMS), limit=max(limit, 5))
        if not filings:
            return {"status": "error", "error": f"No recent insider ownership filings found for {company['title']}"}

        activities = []
        for filing in filings[:limit]:
            parsed = self._parse_ownership_form(await self._fetch_filing_text(filing["filing_url"]))
            activities.append(
                {
                    "form": filing["form"],
                    "filing_date": filing["filing_date"],
                    "report_date": filing["report_date"],
                    "reporting_person": parsed["reporting_person"],
                    "relationship": parsed["relationship"],
                    "transactions": parsed["transactions"][:5],
                    "filing_url": filing["filing_url"],
                }
            )

        return {
            "status": "success",
            "data": {
                "company": company,
                "filings": activities,
            },
        }

    async def activist_watch(self, query: str, limit: int) -> Dict[str, Any]:
        company = await self._resolve_company_record(query)
        if "status" in company and company["status"] == "error":
            return company

        filings = await self._collect_filings(company["cik"], forms=list(ACTIVIST_FORMS), limit=max(limit, 5))
        if not filings:
            return {"status": "error", "error": f"No recent Schedule 13D/13G filings found for {company['title']}"}

        watch_items = []
        for filing in filings[:limit]:
            parsed = self._parse_activist_filing(await self._fetch_filing_text(filing["filing_url"]))
            watch_items.append(
                {
                    "form": filing["form"],
                    "filing_date": filing["filing_date"],
                    "reporting_person": parsed["reporting_person"],
                    "beneficial_ownership": parsed["beneficial_ownership"],
                    "percent_of_class": parsed["percent_of_class"],
                    "item_summary": parsed["item_summary"],
                    "filing_url": filing["filing_url"],
                }
            )

        return {
            "status": "success",
            "data": {
                "company": company,
                "filings": watch_items,
            },
        }

    async def institutional_holders(self, query: str, limit: int) -> Dict[str, Any]:
        company = await self._resolve_company_record(query)
        if "status" in company and company["status"] == "error":
            return company

        zip_path = await self._ensure_latest_13f_zip()
        archive = zipfile.ZipFile(zip_path)
        try:
            submissions = self._parse_13f_tsv_map(archive, "SUBMISSION.tsv")
            coverpage = self._parse_13f_tsv_map(archive, "COVERPAGE.tsv")
            summarypage = self._parse_13f_tsv_map(archive, "SUMMARYPAGE.tsv")

            target_name = _normalize_company_name(company["title"])
            target_strict_name = _normalize_issuer_name(company["title"])
            holders: Dict[str, Dict[str, Any]] = {}

            with archive.open("INFOTABLE.tsv") as raw:
                reader = csv.DictReader(TextIOWrapper(raw, encoding="utf-8"), delimiter="\t")
                for row in reader:
                    issuer_name = _normalize_company_name(row["NAMEOFISSUER"])
                    issuer_strict_name = _normalize_issuer_name(row["NAMEOFISSUER"])
                    if issuer_strict_name != target_strict_name and issuer_name != target_name:
                        continue
                    if row["PUTCALL"]:
                        continue

                    accession_number = row["ACCESSION_NUMBER"]
                    manager = coverpage.get(accession_number, {})
                    summary = summarypage.get(accession_number, {})
                    submission = submissions.get(accession_number, {})
                    manager_name = manager.get("FILINGMANAGER_NAME", accession_number)
                    key = f"{accession_number}|{manager_name}"
                    reported_value = _safe_int(row["VALUE"]) or 0
                    reported_shares = _safe_int(row["SSHPRNAMT"]) or 0

                    if key not in holders:
                        holders[key] = {
                            "filing_manager_name": manager_name,
                            "accession_number": accession_number,
                            "filing_date": submission.get("FILING_DATE", ""),
                            "period_of_report": manager.get("REPORTCALENDARORQUARTER", ""),
                            "report_type": manager.get("REPORTTYPE", ""),
                            "issuer_name_matched": row["NAMEOFISSUER"],
                            "reported_value_usd": 0,
                            "reported_shares": 0,
                            "table_entry_total": _safe_int(summary.get("TABLEENTRYTOTAL", "")),
                            "table_value_total": _safe_int(summary.get("TABLEVALUETOTAL", "")),
                        }
                    holders[key]["reported_value_usd"] += reported_value
                    holders[key]["reported_shares"] += reported_shares

            holder_rows = list(holders.values())
            holder_rows.sort(key=lambda row: row["reported_value_usd"], reverse=True)
            if not holder_rows:
                return {
                    "status": "error",
                    "error": f"No 13F issuer rows matched {company['title']} in the latest SEC dataset",
                }

            return {
                "status": "success",
                "data": {
                    "company": company,
                    "match_method": "latest SEC 13F flattened dataset issuer-name normalization",
                    "dataset_zip": str(zip_path),
                    "holder_count": len(holder_rows),
                    "top_holders": holder_rows[:limit],
                },
            }
        finally:
            archive.close()
