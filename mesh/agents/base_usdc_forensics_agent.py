import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from google.cloud import bigquery

from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()

USDC_BASE = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"


class BaseUSDCForensicsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.project_id = os.getenv("BIGQUERY_PROJECT_ID")
        if not self.project_id:
            raise ValueError("BIGQUERY_PROJECT_ID environment variable is required")

        gcp_creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if gcp_creds_path:
            logger.info(f"Using GCP credentials from: {gcp_creds_path}")
        else:
            logger.warning("GOOGLE_APPLICATION_CREDENTIALS not set, using default credentials")

        self.table = f"{self.project_id}.base_blockchain___community_public_dataset.token_transfers"
        self.client = bigquery.Client(project=self.project_id)

        self.metadata.update(
            {
                "name": "Base USDC Forensics Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Reveal USDC transaction patterns for any addresses on Base. This agent is your dedicated onchain USDC investigator for the Base network, combining BigQuery data access with a curated set of forensic tools.",
                "external_apis": ["Google BigQuery"],
                "tags": ["Blockchain", "Forensics", "USDC", "Base", "x402"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Base.png",
                "examples": [
                    "Show me the USDC profile for 0x7d9d1821d15b9e0b8ab98a058361233e255e405d",
                    "Who are the top USDC funders for this address?",
                    "Where does this wallet send its USDC?",
                    "Show daily USDC activity for this address",
                ],
                "credits": 3,
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                },
            }
        )

    def get_system_prompt(self) -> str:
        return """You are a blockchain forensics analyst specializing in USDC transaction analysis on the Base network.

            You have access to six powerful forensic tools:
            1. usdc_basic_profile - Get a wallet's USDC activity summary (first/last seen, total in/out, net flow)
            2. usdc_top_funders - Find where USDC comes from (top source wallets)
            3. usdc_top_sinks - Find where USDC goes (top destination wallets)
            4. usdc_net_counterparties - Per-counterparty net flow analysis (who is this wallet paying vs receiving from)
            5. usdc_daily_activity - Daily transaction patterns (volume spikes, active periods)
            6. usdc_hourly_pair_activity - Hourly flows between two specific addresses

            When analyzing results:
            - Highlight unusual patterns like concentrated funding sources or circular flows
            - Note timing patterns that might indicate bot activity or wash trading
            - Identify hub wallets and potential controller addresses
            - Present monetary values clearly with USDC denomination
            - Format addresses as clickable links when presenting results

        Always provide actionable forensic insights based on the data."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "usdc_basic_profile",
                    "description": "Get a wallet's USDC activity summary on Base: first/last seen timestamps, total transfer count, aggregate USDC in/out and net flow. Use this for a quick financial snapshot before drilling into details.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "address": {
                                "type": "string",
                                "description": "Wallet address starting with 0x",
                            }
                        },
                        "required": ["address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "usdc_top_funders",
                    "description": "Identify the top source wallets that send USDC to the target address, including counts, total volume, and time range. Use to detect concentrated funding patterns and surface potential hub/controller wallets.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "address": {
                                "type": "string",
                                "description": "Wallet address starting with 0x",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of funders to return (default 50)",
                                "default": 50,
                            },
                        },
                        "required": ["address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "usdc_top_sinks",
                    "description": "Find the main destinations where the target wallet sends USDC, showing transfer counts and volumes per counterparty. Use to understand fund flow destinations and reveal payout hubs.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "address": {
                                "type": "string",
                                "description": "Wallet address starting with 0x",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of sinks to return (default 50)",
                                "default": 50,
                            },
                        },
                        "required": ["address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "usdc_net_counterparties",
                    "description": "Compute per-counterparty net flow metrics showing whether the wallet is a net payer or receiver for each connected address. Use to rank counterparties by economic importance and spot asymmetric relationships.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "address": {
                                "type": "string",
                                "description": "Wallet address starting with 0x",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of counterparties to return (default 100)",
                                "default": 100,
                            },
                        },
                        "required": ["address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "usdc_daily_activity",
                    "description": "Aggregate a wallet's USDC activity by calendar day, returning daily transaction counts and total volume received/sent. Use to spot active vs quiet periods and unusual volume spikes.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "address": {
                                "type": "string",
                                "description": "Wallet address starting with 0x",
                            }
                        },
                        "required": ["address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "usdc_hourly_pair_activity",
                    "description": "Report hourly USDC transfer activity between two specific addresses, showing volume in each direction (A→B and B→A) per hour. Use to analyze flow intensity between suspected related wallets.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "address_a": {
                                "type": "string",
                                "description": "First wallet address starting with 0x",
                            },
                            "address_b": {
                                "type": "string",
                                "description": "Second wallet address starting with 0x",
                            },
                        },
                        "required": ["address_a", "address_b"],
                    },
                },
            },
        ]

    def _run_query(self, query: str, params: List[bigquery.ScalarQueryParameter]) -> List[Dict[str, Any]]:
        job_config = bigquery.QueryJobConfig(query_parameters=params)
        job = self.client.query(query, job_config=job_config)
        df = job.to_dataframe()
        for col in df.columns:
            if df[col].dtype == "datetime64[ns, UTC]" or "timestamp" in col.lower() or "time" in col.lower():
                df[col] = df[col].astype(str)
            if "date" in col.lower():
                df[col] = df[col].astype(str)
        return df.to_dict(orient="records")

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def usdc_basic_profile(self, address: str) -> Dict[str, Any]:
        addr = address.lower()
        query = f"""
        WITH params AS (
          SELECT
            @addr AS addr,
            @usdc AS usdc
        ),
        usdc_transfers AS (
          SELECT
            block_timestamp,
            block_number,
            transaction_hash,
            transaction_index,
            event_index,
            address,
            from_address,
            to_address,
            SAFE_CAST(quantity AS NUMERIC) AS quantity_raw
          FROM `{self.table}` t
          CROSS JOIN params p
          WHERE t.event_type = 'ERC-20'
            AND t.address = p.usdc
        ),
        addr_txs AS (
          SELECT *
          FROM usdc_transfers t
          CROSS JOIN params p
          WHERE t.from_address = p.addr
             OR t.to_address   = p.addr
        )
        SELECT
          (SELECT addr FROM params) AS address,
          MIN(block_timestamp)      AS first_seen,
          MAX(block_timestamp)      AS last_seen,
          COUNT(*)                  AS total_txs,
          COUNTIF(to_address   = (SELECT addr FROM params)) AS in_tx_count,
          COUNTIF(from_address = (SELECT addr FROM params)) AS out_tx_count,
          SUM(CASE WHEN to_address   = (SELECT addr FROM params)
                   THEN quantity_raw ELSE 0 END) / 1e6 AS total_in_usdc,
          SUM(CASE WHEN from_address = (SELECT addr FROM params)
                   THEN quantity_raw ELSE 0 END) / 1e6 AS total_out_usdc,
          SUM(CASE
                WHEN to_address   = (SELECT addr FROM params) THEN quantity_raw
                WHEN from_address = (SELECT addr FROM params) THEN -quantity_raw
                ELSE 0
              END) / 1e6 AS net_flow_usdc
        FROM addr_txs;
        """
        params = [
            bigquery.ScalarQueryParameter("addr", "STRING", addr),
            bigquery.ScalarQueryParameter("usdc", "STRING", USDC_BASE),
        ]
        result = self._run_query(query, params)
        return {"status": "success", "data": result[0] if result else {}}

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def usdc_top_funders(self, address: str, limit: int = 50) -> Dict[str, Any]:
        addr = address.lower()
        query = f"""
        WITH params AS (
          SELECT @addr AS addr, @usdc AS usdc
        ),
        usdc_in AS (
          SELECT
            block_timestamp,
            from_address,
            SAFE_CAST(quantity AS NUMERIC) AS quantity_raw
          FROM `{self.table}` t
          CROSS JOIN params p
          WHERE t.event_type = 'ERC-20'
            AND t.address = p.usdc
            AND t.to_address = p.addr
        )
        SELECT
          from_address AS funder,
          COUNT(*) AS tx_count,
          SUM(quantity_raw) / 1e6 AS total_received_usdc,
          MIN(block_timestamp) AS first_time,
          MAX(block_timestamp) AS last_time
        FROM usdc_in
        GROUP BY funder
        ORDER BY total_received_usdc DESC
        LIMIT {limit};
        """
        params = [
            bigquery.ScalarQueryParameter("addr", "STRING", addr),
            bigquery.ScalarQueryParameter("usdc", "STRING", USDC_BASE),
        ]
        result = self._run_query(query, params)
        return {"status": "success", "data": result}

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def usdc_top_sinks(self, address: str, limit: int = 50) -> Dict[str, Any]:
        addr = address.lower()
        query = f"""
        WITH params AS (
          SELECT @addr AS addr, @usdc AS usdc
        ),
        usdc_out AS (
          SELECT
            block_timestamp,
            to_address,
            SAFE_CAST(quantity AS NUMERIC) AS quantity_raw
          FROM `{self.table}` t
          CROSS JOIN params p
          WHERE t.event_type = 'ERC-20'
            AND t.address = p.usdc
            AND t.from_address = p.addr
        )
        SELECT
          to_address AS counterparty,
          COUNT(*) AS tx_count,
          SUM(quantity_raw) / 1e6 AS total_sent_usdc,
          MIN(block_timestamp) AS first_time,
          MAX(block_timestamp) AS last_time
        FROM usdc_out
        GROUP BY counterparty
        ORDER BY total_sent_usdc DESC
        LIMIT {limit};
        """
        params = [
            bigquery.ScalarQueryParameter("addr", "STRING", addr),
            bigquery.ScalarQueryParameter("usdc", "STRING", USDC_BASE),
        ]
        result = self._run_query(query, params)
        return {"status": "success", "data": result}

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def usdc_net_counterparties(self, address: str, limit: int = 100) -> Dict[str, Any]:
        addr = address.lower()
        query = f"""
        WITH params AS (
          SELECT @addr AS addr, @usdc AS usdc
        ),
        usdc_transfers AS (
          SELECT
            block_timestamp,
            from_address,
            to_address,
            SAFE_CAST(quantity AS NUMERIC) AS quantity_raw
          FROM `{self.table}` t
          CROSS JOIN params p
          WHERE t.event_type = 'ERC-20'
            AND t.address = p.usdc
            AND (t.from_address = p.addr OR t.to_address = p.addr)
        ),
        edges AS (
          SELECT
            CASE
              WHEN to_address   = addr THEN from_address
              WHEN from_address = addr THEN to_address
            END AS counterparty,
            CASE
              WHEN to_address   = addr THEN 'in'
              ELSE 'out'
            END AS direction,
            quantity_raw AS value_raw
          FROM usdc_transfers, params
        )
        SELECT
          counterparty,
          COUNT(*) AS tx_count,
          SUM(CASE WHEN direction = 'in'  THEN value_raw ELSE 0 END) / 1e6 AS total_in_usdc,
          SUM(CASE WHEN direction = 'out' THEN value_raw ELSE 0 END) / 1e6 AS total_out_usdc,
          SUM(CASE WHEN direction = 'in'
                   THEN value_raw ELSE -value_raw END) / 1e6          AS net_flow_usdc
        FROM edges
        GROUP BY counterparty
        ORDER BY GREATEST(total_in_usdc, total_out_usdc) DESC
        LIMIT {limit};
        """
        params = [
            bigquery.ScalarQueryParameter("addr", "STRING", addr),
            bigquery.ScalarQueryParameter("usdc", "STRING", USDC_BASE),
        ]
        result = self._run_query(query, params)
        return {"status": "success", "data": result}

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def usdc_daily_activity(self, address: str) -> Dict[str, Any]:
        addr = address.lower()
        query = f"""
        WITH params AS (
          SELECT @addr AS addr, @usdc AS usdc
        ),
        usdc_transfers AS (
          SELECT
            block_timestamp,
            from_address,
            to_address,
            SAFE_CAST(quantity AS NUMERIC) AS quantity_raw
          FROM `{self.table}` t
          CROSS JOIN params p
          WHERE t.event_type = 'ERC-20'
            AND t.address = p.usdc
            AND (t.from_address = p.addr OR t.to_address = p.addr)
        )
        SELECT
          DATE(block_timestamp) AS tx_date,
          COUNT(*) AS tx_count,
          SUM(CASE WHEN to_address   = (SELECT addr FROM params)
                   THEN quantity_raw ELSE 0 END) / 1e6 AS in_usdc,
          SUM(CASE WHEN from_address = (SELECT addr FROM params)
                   THEN quantity_raw ELSE 0 END) / 1e6 AS out_usdc
        FROM usdc_transfers
        GROUP BY tx_date
        ORDER BY tx_date;
        """
        params = [
            bigquery.ScalarQueryParameter("addr", "STRING", addr),
            bigquery.ScalarQueryParameter("usdc", "STRING", USDC_BASE),
        ]
        result = self._run_query(query, params)
        return {"status": "success", "data": result}

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def usdc_hourly_pair_activity(self, address_a: str, address_b: str) -> Dict[str, Any]:
        addr_a = address_a.lower()
        addr_b = address_b.lower()
        query = f"""
        WITH params AS (
          SELECT @addr_a AS addr_a, @addr_b AS addr_b, @usdc AS usdc
        ),
        usdc_pair AS (
          SELECT
            block_timestamp,
            from_address,
            to_address,
            SAFE_CAST(quantity AS NUMERIC) AS quantity_raw
          FROM `{self.table}` t
          CROSS JOIN params p
          WHERE t.event_type = 'ERC-20'
            AND t.address = p.usdc
            AND (
              (t.from_address = addr_a AND t.to_address = addr_b) OR
              (t.from_address = addr_b AND t.to_address = addr_a)
            )
        )
        SELECT
          TIMESTAMP_TRUNC(block_timestamp, HOUR) AS hour_bucket,
          COUNT(*) AS tx_count,
          SUM(CASE WHEN from_address = addr_a AND to_address = addr_b
                   THEN quantity_raw ELSE 0 END) / 1e6 AS a_to_b_usdc,
          SUM(CASE WHEN from_address = addr_b AND to_address = addr_a
                   THEN quantity_raw ELSE 0 END) / 1e6 AS b_to_a_usdc
        FROM usdc_pair, params
        GROUP BY hour_bucket
        ORDER BY hour_bucket;
        """
        params = [
            bigquery.ScalarQueryParameter("addr_a", "STRING", addr_a),
            bigquery.ScalarQueryParameter("addr_b", "STRING", addr_b),
            bigquery.ScalarQueryParameter("usdc", "STRING", USDC_BASE),
        ]
        result = self._run_query(query, params)
        return {"status": "success", "data": result}

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name == "usdc_basic_profile":
            address = function_args.get("address")
            if not address:
                return {"status": "error", "error": "Missing 'address' parameter"}
            return await self.usdc_basic_profile(address)

        elif tool_name == "usdc_top_funders":
            address = function_args.get("address")
            limit = function_args.get("limit", 50)
            if not address:
                return {"status": "error", "error": "Missing 'address' parameter"}
            return await self.usdc_top_funders(address, limit)

        elif tool_name == "usdc_top_sinks":
            address = function_args.get("address")
            limit = function_args.get("limit", 50)
            if not address:
                return {"status": "error", "error": "Missing 'address' parameter"}
            return await self.usdc_top_sinks(address, limit)

        elif tool_name == "usdc_net_counterparties":
            address = function_args.get("address")
            limit = function_args.get("limit", 100)
            if not address:
                return {"status": "error", "error": "Missing 'address' parameter"}
            return await self.usdc_net_counterparties(address, limit)

        elif tool_name == "usdc_daily_activity":
            address = function_args.get("address")
            if not address:
                return {"status": "error", "error": "Missing 'address' parameter"}
            return await self.usdc_daily_activity(address)

        elif tool_name == "usdc_hourly_pair_activity":
            address_a = function_args.get("address_a")
            address_b = function_args.get("address_b")
            if not address_a or not address_b:
                return {"status": "error", "error": "Missing 'address_a' or 'address_b' parameter"}
            return await self.usdc_hourly_pair_activity(address_a, address_b)

        else:
            return {"status": "error", "error": f"Unsupported tool: {tool_name}"}
