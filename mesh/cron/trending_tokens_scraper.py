"""
Trending Tokens Scraper
Fetches top 20 trending tokens from DexScreener for multiple chains and uploads to R2
Designed to run as a PM2 cron job
"""

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import json
import time
import os
import logging
import boto3
from datetime import datetime
from typing import List, Dict, Optional
import asyncio
import aiohttp
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
CHAINS = {
    'solana': 'https://dexscreener.com/solana',
    'bsc': 'https://dexscreener.com/bsc',
    'ethereum': 'https://dexscreener.com/ethereum',
    'base': 'https://dexscreener.com/base'
}

TOP_N_TOKENS = 20
RATE_LIMIT_DELAY = 0.5  # 500ms between API calls (well below 300 req/min limit)
PAGE_LOAD_WAIT = 30  # Wait time for Cloudflare check
R2_BUCKET = 'mesh'

# R2 Configuration from environment
R2_ENDPOINT = os.getenv('R2_ENDPOINT')
R2_ACCESS_KEY = os.getenv('R2_ACCESS_KEY')
R2_SECRET_KEY = os.getenv('R2_SECRET_KEY')


class TrendingTokensScraper:
    """Scrapes trending tokens from DexScreener and uploads to R2"""

    def __init__(self):
        self.s3_client = self._init_s3_client()
        self.session = None

    def _init_s3_client(self):
        """Initialize boto3 S3 client for R2"""
        if not all([R2_ENDPOINT, R2_ACCESS_KEY, R2_SECRET_KEY]):
            raise ValueError("R2 credentials not found in environment variables")

        return boto3.client(
            's3',
            endpoint_url=R2_ENDPOINT,
            aws_access_key_id=R2_ACCESS_KEY,
            aws_secret_access_key=R2_SECRET_KEY,
            region_name='auto'
        )

    async def _init_session(self):
        """Initialize aiohttp session"""
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def _close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
            self.session = None

    def scrape_trending_pairs(self, chain: str, url: str) -> List[str]:
        """
        Scrape trending pair addresses from DexScreener using browser automation

        Args:
            chain: Chain identifier (solana, bsc, ethereum, base)
            url: DexScreener URL for the chain

        Returns:
            List of pair addresses
        """
        logger.info(f"Scraping {chain} trending pairs from {url}")

        # Configure Chrome options
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--window-size=1920,1080')

        driver = None
        pair_addresses = []

        try:
            driver = uc.Chrome(options=options, use_subprocess=True)

            logger.info(f"Navigating to: {url}")
            driver.get(url)

            # Wait for Cloudflare check and page load
            logger.info(f"Waiting for page to load ({PAGE_LOAD_WAIT}s)...")
            time.sleep(PAGE_LOAD_WAIT)

            page_title = driver.title
            logger.info(f"Page loaded: {page_title}")

            if "Just a moment" in page_title:
                logger.warning("Still on Cloudflare check, waiting longer...")
                time.sleep(PAGE_LOAD_WAIT)

            # Get page HTML
            html = driver.page_source

            # Parse HTML
            soup = BeautifulSoup(html, 'html.parser')

            # Find the trending table
            table = soup.find('div', class_='ds-dex-table ds-dex-table-top')

            if not table:
                logger.warning("ds-dex-table-top not found, trying any ds-dex-table...")
                all_tables = soup.find_all('div', class_=lambda x: x and 'ds-dex-table' in x if x else False)
                if all_tables:
                    table = all_tables[0]
                else:
                    logger.error("No dex table found")
                    return []

            # Find all token links in the table
            links = table.find_all('a', href=True)

            for link in links[:TOP_N_TOKENS]:
                href = link.get('href', '')

                # Extract pair address from URL
                # URL format: /solana/{pair_address} or /bsc/{pair_address}, etc.
                if f'/{chain}/' in href:
                    parts = href.split(f'/{chain}/')
                    if len(parts) > 1:
                        pair_address = parts[1].split('?')[0].strip('/')
                        if pair_address:
                            pair_addresses.append(pair_address)

            logger.info(f"Found {len(pair_addresses)} pair addresses for {chain}")

        except Exception as e:
            logger.error(f"Error scraping {chain}: {e}", exc_info=True)

        finally:
            if driver:
                driver.quit()
                logger.info("Browser closed")

        return pair_addresses

    def _is_stable_or_native_token(self, symbol: str, address: str) -> bool:
        """Check if token is a stablecoin or native/wrapped native token"""
        if not symbol:
            return False

        symbol_upper = symbol.upper()

        # Common stablecoins
        stablecoins = ['USDT', 'USDC', 'DAI', 'BUSD', 'TUSD', 'USDD', 'FRAX', 'USDP', 'GUSD', 'PYUSD']

        # Native and wrapped native tokens
        native_tokens = ['SOL', 'WSOL', 'ETH', 'WETH', 'BNB', 'WBNB', 'MATIC', 'WMATIC', 'AVAX', 'WAVAX']

        # Common DEX base tokens
        common_addresses = [
            'So11111111111111111111111111111111111111112',  # Wrapped SOL
            '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'.lower(),  # WETH
            '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'.lower(),  # WBNB
            '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'.lower(),  # USDC on Base
            '0x4200000000000000000000000000000000000006'.lower(),  # WETH on Base
            '0x0b3e328455c4059EEb9e3f84b5543F74E24e7E1b'.lower(),  # Virtual on Base
        ]

        return (symbol_upper in stablecoins or
                symbol_upper in native_tokens or
                address.lower() in common_addresses)

    async def fetch_pair_details(self, chain: str, pair_address: str) -> Optional[Dict]:
        """
        Fetch detailed pair information from DexScreener API
        Returns only token info and social links, selecting the volatile token

        Args:
            chain: Chain identifier
            pair_address: Pair contract address

        Returns:
            Dict with token info or None if not found
        """
        await self._init_session()

        url = f"https://api.dexscreener.com/latest/dex/pairs/{chain}/{pair_address}"

        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()

                    if 'pairs' in data and data['pairs'] and len(data['pairs']) > 0:
                        pair = data['pairs'][0]

                        base_token = pair.get('baseToken', {})
                        quote_token = pair.get('quoteToken', {})

                        # Select the volatile token (not stablecoin or native)
                        base_is_stable = self._is_stable_or_native_token(
                            base_token.get('symbol', ''),
                            base_token.get('address', '')
                        )
                        quote_is_stable = self._is_stable_or_native_token(
                            quote_token.get('symbol', ''),
                            quote_token.get('address', '')
                        )

                        # Token selection logic:
                        # 1. If both are stable/native: skip this pair (return None)
                        # 2. If only quote is stable/native: select base
                        # 3. If only base is stable/native: select quote
                        # 4. If neither are stable/native: select base (default)

                        if base_is_stable and quote_is_stable:
                            # Both are stable/native, skip this pair
                            logger.warning(f"Skipping pair {pair_address}: both tokens are stable/native")
                            return None
                        elif base_is_stable and not quote_is_stable:
                            selected_token = quote_token
                        else:
                            # Either quote is stable (and base is not), or both are volatile
                            # In both cases, pick base token
                            selected_token = base_token

                        # Extract simplified token info
                        result = {
                            'address': selected_token.get('address'),
                            'name': selected_token.get('name'),
                            'symbol': selected_token.get('symbol')
                        }

                        # Add social/info fields if available
                        if 'info' in pair:
                            info = pair['info']
                            links = {}

                            # Add websites
                            if info.get('websites'):
                                links['websites'] = [w.get('url') for w in info['websites'] if w.get('url')]

                            # Add socials
                            if info.get('socials'):
                                for social in info['socials']:
                                    social_type = social.get('type', social.get('platform', ''))
                                    social_url = social.get('url', '')
                                    if social_type and social_url:
                                        if social_type not in links:
                                            links[social_type] = []
                                        links[social_type].append(social_url)

                            if links:
                                result['links'] = links

                        logger.info(f"Fetched details for {chain}/{pair_address}: {result.get('symbol')}")
                        return result
                    else:
                        logger.warning(f"No pair data found for {chain}/{pair_address}")
                        return None
                else:
                    logger.error(f"API error {response.status} for {chain}/{pair_address}")
                    return None

        except Exception as e:
            logger.error(f"Error fetching pair details for {chain}/{pair_address}: {e}")
            return None

    async def process_chain(self, chain: str, url: str) -> List[Dict]:
        """
        Process a single chain: scrape pairs and fetch details

        Args:
            chain: Chain identifier
            url: DexScreener URL

        Returns:
            List of token details
        """
        logger.info(f"Processing chain: {chain}")

        # Step 1: Scrape trending pair addresses
        pair_addresses = self.scrape_trending_pairs(chain, url)

        if not pair_addresses:
            logger.warning(f"No pair addresses found for {chain}")
            return []

        # Step 2: Fetch details for each pair with rate limiting
        token_details = []

        for i, pair_address in enumerate(pair_addresses, 1):
            logger.info(f"Fetching details for {chain} pair {i}/{len(pair_addresses)}: {pair_address}")

            details = await self.fetch_pair_details(chain, pair_address)

            if details:
                token_details.append(details)

            # Rate limiting
            if i < len(pair_addresses):
                await asyncio.sleep(RATE_LIMIT_DELAY)

        logger.info(f"Completed {chain}: {len(token_details)} tokens with full details")
        return token_details

    def upload_to_r2(self, chain: str, tokens: List[Dict]):
        """
        Upload chain data to R2 bucket as a single file per chain

        Args:
            chain: Chain identifier (solana, bsc, ethereum, base)
            tokens: List of token data
        """
        try:
            data = {
                'chain': chain,
                'last_updated': datetime.now().isoformat(),
                'tokens': tokens
            }

            json_data = json.dumps(data, indent=2, ensure_ascii=False)

            filename = f"trending_tokens_{chain}.json"

            self.s3_client.put_object(
                Bucket=R2_BUCKET,
                Key=filename,
                Body=json_data.encode('utf-8'),
                ContentType='application/json'
            )

            logger.info(f"Uploaded {filename} to R2 bucket {R2_BUCKET} ({len(tokens)} tokens)")

        except Exception as e:
            logger.error(f"Error uploading {chain} to R2: {e}", exc_info=True)

    async def run(self):
        """Main execution method"""
        logger.info("=" * 80)
        logger.info("TRENDING TOKENS SCRAPER - STARTING")
        logger.info("=" * 80)

        start_time = datetime.now()
        all_results = {}

        try:
            # Process each chain sequentially to avoid overloading
            for chain, url in CHAINS.items():
                logger.info(f"\n{'=' * 80}")
                logger.info(f"Processing: {chain.upper()}")
                logger.info(f"{'=' * 80}")

                token_details = await self.process_chain(chain, url)
                all_results[chain] = token_details

                # Upload to R2 immediately after each chain
                if token_details:
                    self.upload_to_r2(chain, token_details)

                # Add delay between chains to be respectful
                await asyncio.sleep(2)

            # Summary
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            total_tokens = sum(len(tokens) for tokens in all_results.values())

            logger.info("\n" + "=" * 80)
            logger.info("SCRAPING COMPLETED SUCCESSFULLY")
            logger.info("=" * 80)
            logger.info(f"Duration: {duration:.2f} seconds")
            logger.info(f"Total tokens scraped: {total_tokens}")
            for chain, tokens in all_results.items():
                logger.info(f"  {chain}: {len(tokens)} tokens")
            logger.info(f"Files uploaded to R2:")
            for chain in all_results.keys():
                logger.info(f"  - https://mesh-data.heurist.xyz/trending_tokens_{chain}.json")
            logger.info("=" * 80)

        except Exception as e:
            logger.error(f"Error in main execution: {e}", exc_info=True)

        finally:
            await self._close_session()


async def main():
    """Entry point"""
    scraper = TrendingTokensScraper()
    await scraper.run()


if __name__ == "__main__":
    asyncio.run(main())
