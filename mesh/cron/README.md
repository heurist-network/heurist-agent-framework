# Trending Tokens Scraper

Automated cron job that scrapes top 20 trending tokens from DexScreener for multiple chains and uploads the data to Cloudflare R2 storage.

## Overview

This PM2-managed scraper fetches trending token information from DexScreener's UI across 4 major blockchains:
- **Solana**: https://dexscreener.com/solana
- **BSC**: https://dexscreener.com/bsc
- **Ethereum**: https://dexscreener.com/ethereum
- **Base**: https://dexscreener.com/base

Data is stored in R2 bucket `mesh` with one JSON file per chain, containing simplified token information and social links.

## Key Features

### Smart Token Selection
The scraper intelligently selects volatile tokens from trading pairs:
- **Skips pairs** where both tokens are stablecoins/native tokens (USDT/USDC/ETH/SOL/etc.)
- **Prefers volatile tokens** over stablecoins in mixed pairs
- **Defaults to base token** when both tokens are volatile
- **Deduplicates** by token address — multiple pairs resolving to the same token only appear once

**Filtered tokens** (excluded from results):
- Stablecoins: USDT, USDC, DAI, BUSD, TUSD, USDD, FRAX, USDP, GUSD, PYUSD
- Native tokens: SOL, WSOL, ETH, WETH, BNB, WBNB, MATIC, WMATIC, AVAX, WAVAX
- Common addresses: Wrapped SOL, WETH, WBNB, USDC on Base, WETH on Base, Virtual on Base

### Simplified Data Structure
Only stores essential token information:
- Token address, name, and symbol
- Social links (websites, Twitter, Telegram, Discord, etc.)
- **No price data** (avoids stale snapshots)
- Includes `last_updated` timestamp for freshness

### Technical Implementation
- **Cloudflare bypass**: Uses `curl_cffi` with TLS fingerprint impersonation (no browser needed)
- **Concurrent scraping**: All chains scraped in parallel via ThreadPoolExecutor
- **Concurrent API calls**: Pair details fetched with asyncio.gather, capped at 5 concurrent requests
- **Retries**: Up to 3 attempts on both scraping and API calls, with exponential backoff on 429s
- **R2 integration**: Automatic upload of one file per chain

## File Structure

```
/home/appuser/heurist-agent-framework/mesh/cron/
├── trending_tokens_scraper.py   # Main scraper script
├── ecosystem.config.js           # PM2 configuration
├── README.md                    # This file
└── logs/                        # PM2 log files
```

## Setup

### 1. Install Dependencies

```bash
uv pip install curl-cffi beautifulsoup4 boto3 aiohttp python-dotenv
```

No Chrome, xvfb, or browser dependencies required.

### 2. Configure Environment Variables

Ensure the following variables are set in `/home/appuser/heurist-agent-framework/.env`:

```bash
R2_ENDPOINT=https://f85724868ca3f6675d406037f6fad7a2.r2.cloudflarestorage.com
R2_ACCESS_KEY=<your_access_key>
R2_SECRET_KEY=<your_secret_key>
```

### 3. Start with PM2

```bash
cd /home/appuser/heurist-agent-framework/mesh/cron

# Start the cron job
pm2 start ecosystem.config.js

# View status
pm2 status

# View logs
pm2 logs trending-tokens-scraper

# Stop the job
pm2 stop trending-tokens-scraper

# Delete the job
pm2 delete trending-tokens-scraper

# Save PM2 configuration to startup
pm2 save
pm2 startup
```

### 4. Manual Run (for testing)

```bash
cd /home/appuser/heurist-agent-framework
.venv/bin/python mesh/cron/trending_tokens_scraper.py
```

## PM2 Configuration

The job is configured to run every 6 hours using PM2's cron feature:

- **Schedule**: `0 */6 * * *` (every 6 hours)
- **Restart**: Disabled (cron handles scheduling)
- **Memory limit**: 1GB
- **Logs**: Stored in `./logs/` directory

### Modify Schedule

Edit `ecosystem.config.js` and change `cron_restart`:
- Every hour: `0 * * * *`
- Every 3 hours: `0 */3 * * *`
- Every 12 hours: `0 */12 * * *`
- Daily at midnight: `0 0 * * *`

Then reload:
```bash
pm2 reload ecosystem.config.js
```

## R2 Storage

**Bucket**: `mesh`

**Files created** (one per chain):
- `trending_tokens_solana.json`
- `trending_tokens_bsc.json`
- `trending_tokens_ethereum.json`
- `trending_tokens_base.json`

**Example output structure:**
```json
{
  "chain": "ethereum",
  "last_updated": "2025-10-18T12:51:49.658089",
  "tokens": [
    {
      "address": "0x615585c53E43F944E416917D1A5042F07166672C",
      "name": "Yakushima Inu",
      "symbol": "YAKU",
      "links": {
        "websites": [
          "https://yakushimainu.com/"
        ],
        "twitter": [
          "https://twitter.com/YakushimaInu"
        ],
        "telegram": [
          "https://t.me/yakushimainu"
        ]
      }
    }
  ]
}
```

## Token Selection Logic

```python
if base_is_stable and quote_is_stable:
    # Skip this pair entirely (both are stable/native)
    return None
elif base_is_stable and not quote_is_stable:
    # Select quote token (volatile)
    selected_token = quote_token
else:
    # Select base token (either both volatile, or only quote is stable)
    selected_token = base_token
```

## Monitoring

### Check PM2 Status
```bash
pm2 status trending-tokens-scraper
```

### View Logs
```bash
# Real-time logs
pm2 logs trending-tokens-scraper

# Last 100 lines
pm2 logs trending-tokens-scraper --lines 100

# Error logs only
pm2 logs trending-tokens-scraper --err

# Output logs only
pm2 logs trending-tokens-scraper --out
```

### Check Log Files Directly
```bash
# Error log
tail -f /home/appuser/heurist-agent-framework/mesh/cron/logs/trending-tokens-error.log

# Output log
tail -f /home/appuser/heurist-agent-framework/mesh/cron/logs/trending-tokens-out.log
```

## Performance

**Total runtime** (all 4 chains): ~7-10 seconds

Chains are scraped in parallel and API calls are concurrent (5 at a time), so the total runtime is dominated by network latency rather than sequential processing.

## Rate Limits

DexScreener API limits:
- **Rate limit**: 300 requests per minute
- **Script behavior**: 5 concurrent requests with semaphore, exponential backoff on 429s
- **Total requests**: ~80 per run (20 pairs × 4 chains)

## Troubleshooting

### Cloudflare Bypass Fails
If `curl_cffi` stops working (Cloudflare updates their detection):
- Update `curl_cffi`: `uv pip install --upgrade curl-cffi`
- Try a different impersonation target in the script (e.g. `chrome110`, `safari`)

### API Rate Limiting
If you hit rate limits:
- The script automatically backs off with exponential delay on 429 responses
- Reduce `API_CONCURRENCY` in the script if needed

### R2 Upload Errors
Check R2 credentials:
```bash
grep "R2_" /home/appuser/heurist-agent-framework/.env
```

### Memory Issues
If the job runs out of memory:
- Adjust `max_memory_restart` in `ecosystem.config.js`
- Consider reducing `TOP_N_TOKENS` in the script

## Maintenance

### Update Script
After modifying `trending_tokens_scraper.py`:
```bash
pm2 restart trending-tokens-scraper
```

### View Next Run Time
```bash
pm2 show trending-tokens-scraper | grep "cron"
```

## Integration

To use this data in other applications:

### Fetch Latest Data
```python
import boto3
import json
import os

s3 = boto3.client(
    's3',
    endpoint_url=os.getenv('R2_ENDPOINT'),
    aws_access_key_id=os.getenv('R2_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('R2_SECRET_KEY'),
    region_name='auto'
)

# Fetch Ethereum trending tokens
response = s3.get_object(Bucket='mesh', Key='trending_tokens_ethereum.json')
data = json.loads(response['Body'].read())

# Access data
chain = data['chain']  # 'ethereum'
last_updated = data['last_updated']
tokens = data['tokens']

for token in tokens[:5]:
    print(f"{token['symbol']}: {token['name']}")
    print(f"  Address: {token['address']}")
    if 'links' in token:
        print(f"  Links: {token['links']}")
```
