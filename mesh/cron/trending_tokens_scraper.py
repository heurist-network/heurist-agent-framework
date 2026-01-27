"""
Get Trending Tokens
Fetches top 20 trending tokens from DexScreener for multiple chains and uploads to R2.
Designed to run as a PM2 cron job.
"""

import asyncio
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Dict, List, Optional

import aiohttp
import boto3
from bs4 import BeautifulSoup
from curl_cffi import requests as cffi_requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

CHAINS = {
    "solana": "https://dexscreener.com/solana",
    "bsc": "https://dexscreener.com/bsc",
    "ethereum": "https://dexscreener.com/ethereum",
    "base": "https://dexscreener.com/base",
}

TOP_N_TOKENS = 20
MAX_RETRIES = 3
# DexScreener API allows 300 req/min — 5 concurrent is conservative
API_CONCURRENCY = 5
R2_BUCKET = "mesh"

R2_ENDPOINT = os.getenv("R2_ENDPOINT")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")

STABLECOINS = frozenset(["USDT", "USDC", "DAI", "BUSD", "TUSD", "USDD", "FRAX", "USDP", "GUSD", "PYUSD"])
NATIVE_TOKENS = frozenset(["SOL", "WSOL", "ETH", "WETH", "BNB", "WBNB", "MATIC", "WMATIC", "AVAX", "WAVAX"])
KNOWN_BASE_ADDRESSES = frozenset(
    [
        "So11111111111111111111111111111111111111112",  # Wrapped SOL
        "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",  # WETH
        "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c",  # WBNB
        "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",  # USDC on Base
        "0x4200000000000000000000000000000000000006",  # WETH on Base
        "0x0b3e328455c4059eeb9e3f84b5543f74e24e7e1b",  # Virtual on Base
    ]
)


class TrendingTokensScraper:
    """Scrapes trending tokens from DexScreener and uploads to R2"""

    def __init__(self):
        self.s3_client = self._init_s3_client()

    def _init_s3_client(self):
        if not all([R2_ENDPOINT, R2_ACCESS_KEY, R2_SECRET_KEY]):
            raise ValueError("R2 credentials not found in environment variables")

        return boto3.client(
            "s3",
            endpoint_url=R2_ENDPOINT,
            aws_access_key_id=R2_ACCESS_KEY,
            aws_secret_access_key=R2_SECRET_KEY,
            region_name="auto",
        )

    def _scrape_trending_pairs(self, chain: str, url: str) -> List[str]:
        """
        Scrape trending pair addresses from DexScreener using curl_cffi.
        Bypasses Cloudflare via TLS fingerprint impersonation — no browser needed.
        Retries up to MAX_RETRIES on failure.
        """
        logger.info(f"Scraping {chain} trending pairs from {url}")

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = cffi_requests.get(url, impersonate="chrome", timeout=30)

                if response.status_code != 200:
                    logger.warning(f"HTTP {response.status_code} for {url} (attempt {attempt}/{MAX_RETRIES})")
                    continue

                if "Just a moment" in response.text:
                    logger.warning(f"Cloudflare challenge hit for {chain} (attempt {attempt}/{MAX_RETRIES})")
                    continue

                soup = BeautifulSoup(response.text, "html.parser")

                table = soup.find("div", class_="ds-dex-table ds-dex-table-top")
                if not table:
                    all_tables = soup.find_all("div", class_=lambda x: x and "ds-dex-table" in x if x else False)
                    table = all_tables[0] if all_tables else None

                if not table:
                    logger.warning(f"No dex table found for {chain} (attempt {attempt}/{MAX_RETRIES})")
                    continue

                seen = set()
                pair_addresses = []
                for link in table.find_all("a", href=True):
                    href = link.get("href", "")
                    if f"/{chain}/" not in href:
                        continue
                    parts = href.split(f"/{chain}/")
                    if len(parts) < 2:
                        continue
                    addr = parts[1].split("?")[0].strip("/")
                    if addr and addr not in seen:
                        seen.add(addr)
                        pair_addresses.append(addr)
                    if len(pair_addresses) >= TOP_N_TOKENS:
                        break

                logger.info(f"Found {len(pair_addresses)} pair addresses for {chain}")
                return pair_addresses

            except Exception as e:
                logger.warning(f"Error scraping {chain} (attempt {attempt}/{MAX_RETRIES}): {e}")

        logger.error(f"Failed to scrape {chain} after {MAX_RETRIES} attempts")
        return []

    @staticmethod
    def _is_stable_or_native(symbol: str, address: str) -> bool:
        if not symbol:
            return False
        upper = symbol.upper()
        return upper in STABLECOINS or upper in NATIVE_TOKENS or address.lower() in KNOWN_BASE_ADDRESSES

    @staticmethod
    def _extract_token_result(pair: Dict) -> Optional[Dict]:
        """Pick the volatile token from a pair and extract its info + links."""
        base = pair.get("baseToken", {})
        quote = pair.get("quoteToken", {})

        base_stable = TrendingTokensScraper._is_stable_or_native(base.get("symbol", ""), base.get("address", ""))
        quote_stable = TrendingTokensScraper._is_stable_or_native(quote.get("symbol", ""), quote.get("address", ""))

        if base_stable and quote_stable:
            return None

        selected = quote if (base_stable and not quote_stable) else base

        result = {
            "address": selected.get("address"),
            "name": selected.get("name"),
            "symbol": selected.get("symbol"),
        }

        info = pair.get("info")
        if info:
            links = {}
            if info.get("websites"):
                links["websites"] = [w["url"] for w in info["websites"] if w.get("url")]
            for social in info.get("socials", []):
                stype = social.get("type", social.get("platform", ""))
                surl = social.get("url", "")
                if stype and surl:
                    links.setdefault(stype, []).append(surl)
            if links:
                result["links"] = links

        return result

    async def _fetch_pair_details(
        self, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, chain: str, pair_address: str
    ) -> Optional[Dict]:
        url = f"https://api.dexscreener.com/latest/dex/pairs/{chain}/{pair_address}"

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                async with semaphore:
                    async with session.get(url) as response:
                        if response.status == 429:
                            wait = 2**attempt
                            logger.warning(f"Rate limited on {chain}/{pair_address}, backing off {wait}s")
                            await asyncio.sleep(wait)
                            continue

                        if response.status != 200:
                            logger.warning(f"API {response.status} for {chain}/{pair_address} (attempt {attempt})")
                            continue

                        data = await response.json()

                pairs = data.get("pairs")
                if not pairs:
                    logger.warning(f"No pair data for {chain}/{pair_address}")
                    return None

                result = self._extract_token_result(pairs[0])
                if result:
                    logger.info(f"Fetched {chain}/{pair_address}: {result.get('symbol')}")
                else:
                    logger.warning(f"Skipping {chain}/{pair_address}: both tokens are stable/native")
                return result

            except Exception as e:
                logger.warning(f"Error fetching {chain}/{pair_address} (attempt {attempt}): {e}")

        logger.error(f"Failed to fetch {chain}/{pair_address} after {MAX_RETRIES} attempts")
        return None

    async def _process_chain(
        self, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, chain: str, url: str
    ) -> List[Dict]:
        logger.info(f"Processing chain: {chain}")

        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor(max_workers=1) as pool:
            pair_addresses = await loop.run_in_executor(pool, self._scrape_trending_pairs, chain, url)

        if not pair_addresses:
            logger.warning(f"No pair addresses found for {chain}")
            return []

        tasks = [self._fetch_pair_details(session, semaphore, chain, addr) for addr in pair_addresses]
        results = await asyncio.gather(*tasks)

        # Dedup by token address — multiple pairs can resolve to the same token
        seen_addresses = set()
        token_details = []
        for r in results:
            if r is None:
                continue
            addr = r.get("address", "").lower()
            if addr in seen_addresses:
                continue
            seen_addresses.add(addr)
            token_details.append(r)

        logger.info(f"Completed {chain}: {len(token_details)} unique tokens")
        return token_details

    def upload_to_r2(self, chain: str, tokens: List[Dict]):
        try:
            data = {"chain": chain, "last_updated": datetime.now().isoformat(), "tokens": tokens}
            json_data = json.dumps(data, indent=2, ensure_ascii=False)
            filename = f"trending_tokens_{chain}.json"

            self.s3_client.put_object(
                Bucket=R2_BUCKET, Key=filename, Body=json_data.encode("utf-8"), ContentType="application/json"
            )
            logger.info(f"Uploaded {filename} to R2 ({len(tokens)} tokens)")

        except Exception as e:
            logger.error(f"Error uploading {chain} to R2: {e}", exc_info=True)

    async def run(self):
        logger.info("=" * 80)
        logger.info("TRENDING TOKENS SCRAPER - STARTING")
        logger.info("=" * 80)

        start_time = datetime.now()
        semaphore = asyncio.Semaphore(API_CONCURRENCY)

        async with aiohttp.ClientSession() as session:
            # Scrape all chains in parallel, then fetch pair details concurrently
            chain_tasks = {
                chain: self._process_chain(session, semaphore, chain, url) for chain, url in CHAINS.items()
            }
            all_results = {}
            for chain, task in chain_tasks.items():
                all_results[chain] = await task

            for chain, tokens in all_results.items():
                if tokens:
                    self.upload_to_r2(chain, tokens)

        duration = (datetime.now() - start_time).total_seconds()
        total_tokens = sum(len(t) for t in all_results.values())

        logger.info("=" * 80)
        logger.info("SCRAPING COMPLETED")
        logger.info(f"Duration: {duration:.2f}s | Total tokens: {total_tokens}")
        for chain, tokens in all_results.items():
            logger.info(f"  {chain}: {len(tokens)} tokens")
        logger.info("=" * 80)


async def main():
    scraper = TrendingTokensScraper()
    await scraper.run()


if __name__ == "__main__":
    asyncio.run(main())
