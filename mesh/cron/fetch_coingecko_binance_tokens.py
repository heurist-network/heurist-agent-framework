"""
Fetch Binance-listed tokens from CoinGecko API and update coingecko_id_map.json
Designed to run as a PM2 cron job
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Set

import aiohttp
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

PRO_API_URL = "https://pro-api.coingecko.com/api/v3"
DATA_DIR = Path(__file__).parent.parent / "data"
MAP_FILE = DATA_DIR / "coingecko_id_map.json"
MAX_PAGES = 20
PAGE_DELAY = 1.5


class CoinGeckoBinanceTokenUpdater:
    """Fetch Binance tokens and update CoinGecko ID mapping"""

    def __init__(self, dry_run=False):
        self.api_key = os.getenv("COINGECKO_API_KEY")
        if not self.api_key:
            raise ValueError("COINGECKO_API_KEY required")
        self.headers = {"x-cg-pro-api-key": self.api_key}
        self.session = None
        self.dry_run = dry_run

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _fetch_binance_tickers_page(self, page: int):
        """Fetch single page of Binance exchange tickers"""
        url = f"{PRO_API_URL}/exchanges/binance/tickers"
        params = {"page": page}

        try:
            async with self.session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("tickers", [])
                else:
                    logger.error(f"API error {response.status} on page {page}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching page {page}: {e}")
            return []

    async def _fetch_all_binance_tickers(self):
        """Fetch all Binance tickers with pagination"""
        all_tickers = []
        page = 1

        while page <= MAX_PAGES:
            logger.info(f"Fetching page {page}...")
            tickers = await self._fetch_binance_tickers_page(page)

            if not tickers:
                logger.info(f"No more tickers on page {page}, stopping pagination")
                break

            all_tickers.extend(tickers)
            logger.info(f"Page {page}: {len(tickers)} tickers, total: {len(all_tickers)}")

            page += 1
            await asyncio.sleep(PAGE_DELAY)

        return all_tickers

    async def _fetch_coin_names(self, coin_ids: Set[str]) -> Dict[str, str]:
        """Fetch coin names for given IDs"""
        url = f"{PRO_API_URL}/coins/list"

        try:
            async with self.session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    all_coins = await response.json()
                    return {coin["id"]: coin["name"] for coin in all_coins if coin["id"] in coin_ids}
                else:
                    logger.error(f"Failed to fetch coin list: {response.status}")
                    return {}
        except Exception as e:
            logger.error(f"Error fetching coin names: {e}")
            return {}

    def _build_ticker_mapping(self, tickers):
        """Build ticker -> coin_id mapping, excluding duplicates"""
        ticker_to_coins = {}

        for ticker_data in tickers:
            coin_id = ticker_data.get("coin_id")
            base = ticker_data.get("base")

            if not coin_id or not base:
                continue

            if base not in ticker_to_coins:
                ticker_to_coins[base] = set()
            ticker_to_coins[base].add(coin_id)

        ticker_mapping = {}
        duplicates = []

        for ticker, coin_ids in ticker_to_coins.items():
            if len(coin_ids) == 1:
                ticker_mapping[ticker] = list(coin_ids)[0]
            else:
                duplicates.append((ticker, coin_ids))

        if duplicates:
            logger.warning(f"Excluding {len(duplicates)} duplicate tickers:")
            for ticker, coin_ids in duplicates[:10]:
                logger.warning(f"  {ticker} -> {coin_ids}")

        return ticker_mapping

    def _build_name_mapping(self, id_to_name: Dict[str, str]) -> Dict[str, str]:
        """Build name -> coin_id mapping, excluding duplicates"""
        name_to_coins = {}

        for coin_id, name in id_to_name.items():
            if name not in name_to_coins:
                name_to_coins[name] = []
            name_to_coins[name].append(coin_id)

        name_mapping = {}
        duplicates = []

        for name, coin_ids in name_to_coins.items():
            if len(coin_ids) == 1:
                name_mapping[name] = coin_ids[0]
            else:
                duplicates.append((name, coin_ids))

        if duplicates:
            logger.warning(f"Excluding {len(duplicates)} duplicate names:")
            for name, coin_ids in duplicates[:10]:
                logger.warning(f"  {name} -> {coin_ids}")

        return name_mapping

    def _load_existing_mapping(self) -> Dict[str, str]:
        """Load existing coingecko_id_map.json"""
        if not MAP_FILE.exists():
            logger.info(f"No existing mapping file at {MAP_FILE}")
            return {}

        try:
            with open(MAP_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading existing mapping: {e}")
            return {}

    def _merge_mappings(self, existing: Dict[str, str], new: Dict[str, str]) -> Dict[str, str]:
        """Merge new mapping into existing, preserving existing entries"""
        merged = existing.copy()
        added = 0
        skipped = 0

        for key, value in new.items():
            if key not in merged:
                merged[key] = value
                added += 1
            elif merged[key] != value:
                logger.warning(f"Conflict: '{key}' exists as '{merged[key]}', new value '{value}' skipped")
                skipped += 1

        logger.info(f"Merge result: {added} added, {skipped} conflicts skipped, {len(existing)} preserved")
        return merged

    def _save_mapping(self, mapping: Dict[str, str]):
        """Save mapping to coingecko_id_map.json"""
        if self.dry_run:
            logger.info(f"DRY RUN: Would save {len(mapping)} entries to {MAP_FILE}")
            logger.info(f"Sample: {dict(list(mapping.items())[:5])}")
            return

        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)

            sorted_mapping = dict(sorted(mapping.items()))

            with open(MAP_FILE, "w") as f:
                json.dump(sorted_mapping, f, indent=2, ensure_ascii=False)
                f.write("\n")

            logger.info(f"Saved {len(mapping)} entries to {MAP_FILE}")
        except Exception as e:
            logger.error(f"Error saving mapping: {e}", exc_info=True)
            raise

    async def run(self):
        """Main execution"""
        logger.info("=" * 80)
        logger.info("COINGECKO BINANCE TOKEN UPDATER - STARTING")
        logger.info(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        logger.info("=" * 80)

        start_time = datetime.now()

        try:
            logger.info("Fetching Binance tickers from CoinGecko...")
            tickers = await self._fetch_all_binance_tickers()
            logger.info(f"Total tickers fetched: {len(tickers)}")

            logger.info("Building ticker mapping...")
            ticker_mapping = self._build_ticker_mapping(tickers)
            logger.info(f"Unique tickers (no duplicates): {len(ticker_mapping)}")

            coin_ids = set(ticker_mapping.values())
            logger.info(f"Fetching names for {len(coin_ids)} coins...")
            id_to_name = await self._fetch_coin_names(coin_ids)
            logger.info(f"Got names for {len(id_to_name)} coins")

            logger.info("Building name mapping...")
            name_mapping = self._build_name_mapping(id_to_name)
            logger.info(f"Unique names (no duplicates): {len(name_mapping)}")

            new_mapping = {**ticker_mapping, **name_mapping}
            logger.info(f"New mapping size: {len(new_mapping)} entries")

            existing_mapping = self._load_existing_mapping()
            logger.info(f"Existing mapping size: {len(existing_mapping)} entries")

            final_mapping = self._merge_mappings(existing_mapping, new_mapping)
            logger.info(f"Final mapping size: {len(final_mapping)} entries")

            self._save_mapping(final_mapping)

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            logger.info("=" * 80)
            logger.info("UPDATE COMPLETED SUCCESSFULLY")
            logger.info(f"Duration: {duration:.2f} seconds")
            logger.info(f"Total entries: {len(final_mapping)}")
            logger.info(f"New entries: {len(final_mapping) - len(existing_mapping)}")
            logger.info("=" * 80)

        except Exception as e:
            logger.error(f"Error in main execution: {e}", exc_info=True)
            raise


async def main():
    dry_run = os.getenv("DRY_RUN", "false").lower() == "true"
    async with CoinGeckoBinanceTokenUpdater(dry_run=dry_run) as updater:
        await updater.run()


if __name__ == "__main__":
    asyncio.run(main())
