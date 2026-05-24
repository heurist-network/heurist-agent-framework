# Base L2 Agent Kit

A DeFi-focused agent for [Heurist Mesh](https://heurist.ai) built on Base L2. Provides token prices, wallet balances, gas estimates, swap routing, liquidity simulation, allowance checks, and flash-loan arbitrage analysis.

## Tools

| Tool | Description | x402 Price |
|------|-------------|------------|
| `get_price` | Token price in USDC via on-chain quoter | $0.003 |
| `get_wallet_balance` | ETH/ERC-20 balance for any address | $0.003 |
| `estimate_gas` | Gas cost in gwei + USD for tx types | $0.002 |
| `swap_tokens` | Token swap with route optimization (simulated) | $0.05 |
| `add_liquidity` | Uniswap V3 LP simulation with impermanent loss | $0.05 |
| `check_allowance` | ERC-20 spender allowance + approval status | $0.002 |
| `simulate_flash_loan` | Multi-DEX arbitrage viability + profit estimate | $0.03 |

## Supported Tokens

ETH, USDC, USDT, DAI, BRETT, DEGEN — plus any ERC-20 by contract address.

## Network

- **Chain:** Base mainnet
- **RPCs:** Public fallbacks + Alchemy
- **Pricing:** Simulated with live on-chain gas estimation

## x402 Pricing

All tools are pay-per-use via [x402](https://github.com/coinbase/x402). Default $0.01/call, tool-specific pricing shown above.

## Metadata

```json
{
  "name": "Base L2 Agent Kit",
  "version": "1.1.0",
  "author": "Manteclaw",
  "author_address": "0x54936DC8D45B5b68eA2EF27dE163D27E3cbC5a83",
  "description": "DeFi toolkit for AI agents on Base L2",
  "tags": ["defi", "base", "trading", "wallet", "ethereum", "swap", "liquidity"],
  "verified": false,
  "x402_config": { "enabled": true, "default_price_usd": "0.01" }
}
```

## Demo

```bash
python3 demo.py
```

## License

MIT
