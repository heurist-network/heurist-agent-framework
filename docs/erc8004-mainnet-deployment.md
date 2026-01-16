# ERC-8004 Mainnet Deployment Guide

## Overview

This guide covers deploying Heurist Mesh agents to Ethereum Mainnet using ERC-8004. The system is already designed to support mainnet - only configuration and environment setup is needed.

## System Readiness Assessment

### What's Already Ready

| Component | Status | Notes |
|-----------|--------|-------|
| CLI | Ready | Already supports `--chain mainnet` |
| Manager | Ready | Chain-agnostic, works with any configured chain |
| R2 Storage | Ready | Same bucket, separate registration files per agent |
| Registry File | Ready | Separate `mainnet: {}` section in `registered_agents.json` |
| Environment Variables | Documented | `ETH_RPC_URL` already in `.env.example` |

### What Needs Configuration

| Item | Action Required |
|------|-----------------|
| Registry Address | Add mainnet contract address to `config.py` |
| RPC URL | Set `ETH_RPC_URL` environment variable |
| Wallet Funding | Fund deployment wallet with mainnet ETH |

## Step-by-Step Deployment Checklist

### Step 1: Update Config with Mainnet Registry Address

Once you receive the mainnet registry contract address, update `mesh/erc8004/config.py`:

```python
CHAIN_CONFIGS: dict[int, ChainConfig] = {
    11155111: {  # Ethereum Sepolia
        "name": "sepolia",
        "rpc_env": "SEPOLIA_RPC_URL",
        "identity_registry": "0x8004A818BFB912233c491871b3d84c89A494BD9e",
        "reputation_registry": "0x8004B663056A597Dffe9eCcC1965A193B7388713",
    },
    1: {  # Ethereum Mainnet
        "name": "mainnet",
        "rpc_env": "ETH_RPC_URL",
        "identity_registry": "0x...",  # <-- ADD MAINNET ADDRESS HERE
        "reputation_registry": "0x...",  # <-- ADD IF AVAILABLE
    },
}
```

### Step 2: Set Environment Variables

Add to your `.env` file:

```bash
# Mainnet RPC (use a reliable provider)
ETH_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY

# Same private key can be used for both networks (or use a different one)
ERC8004_PRIVATE_KEY=0x...

# R2 credentials (already configured)
R2_ENDPOINT=...
R2_ACCESS_KEY=...
R2_SECRET_KEY=...
```

**RPC Provider Recommendations:**
- Alchemy (recommended): `https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY`
- Infura: `https://mainnet.infura.io/v3/YOUR_KEY`
- QuickNode: Your custom endpoint

### Step 3: Fund Deployment Wallet

Check the wallet balance for the address derived from `ERC8004_PRIVATE_KEY`:

```bash
# Get wallet address (optional - use any Ethereum address derivation tool)
cast wallet address $ERC8004_PRIVATE_KEY
```

**Estimated Gas Costs per Agent:**
- Registration: ~200,000-300,000 gas
- At 30 gwei gas price: ~0.006-0.009 ETH per agent
- For 3 agents: ~0.02-0.03 ETH total

**Recommendation:** Fund wallet with at least **0.1 ETH** to cover registrations plus some buffer for future updates.

### Step 4: Dry Run (Preview)

Before actual registration, preview what will happen:

```bash
uv run python -m mesh.erc8004.cli sync --chain mainnet --dry-run
```

Expected output:
```
[DRY RUN] Syncing agents to mainnet (chain 1)...

Registered (3):
  - Token Resolver Agent
  - Trending Token Agent
  - Twitter Intelligence Agent

Summary:
  Registered: 3
  Updated: 0
  Skipped: 0
  Errors: 0
```

### Step 5: Execute Registration

```bash
uv run python -m mesh.erc8004.cli sync --chain mainnet
```

This will:
1. Load all agents with `erc8004.enabled=True`
2. For each agent:
   - Build ERC-8004 compliant registration JSON
   - Upload to R2 storage
   - Register on-chain via agent0 SDK
   - Update R2 with on-chain registration info
   - Save agent ID to local registry file

### Step 6: Verify Registration

Check individual agent status:

```bash
uv run python -m mesh.erc8004.cli status TokenResolverAgent
```

Verify R2 files are updated:

```bash
curl -s https://mesh-data.heurist.xyz/erc8004/TokenResolverAgent.json | jq '.registrations'
```

Expected output should include mainnet registration:
```json
[
  {
    "agentId": 1,
    "agentRegistry": "eip155:1:0x..."
  }
]
```

### Step 7: Update Metadata.json

After registration, trigger the metadata update workflow (automatic on push to main) or manually:

```bash
uv run python .github/scripts/update_mesh_metadata.py --dev
```

This will merge mainnet registration data into `metadata.json`.

## CLI Commands Reference

```bash
# List all eligible agents
uv run python -m mesh.erc8004.cli list --chain mainnet

# Preview sync (no changes made)
uv run python -m mesh.erc8004.cli sync --chain mainnet --dry-run

# Execute sync (register new, update existing)
uv run python -m mesh.erc8004.cli sync --chain mainnet

# Register single agent
uv run python -m mesh.erc8004.cli register TokenResolverAgent --chain mainnet

# Update single agent
uv run python -m mesh.erc8004.cli update TokenResolverAgent --chain mainnet

# Check agent status
uv run python -m mesh.erc8004.cli status TokenResolverAgent
```

## Architecture: How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLI Command                              │
│        uv run python -m mesh.erc8004.cli sync --chain mainnet   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ERC8004Manager                              │
│  • Loads agents with erc8004.enabled=True                       │
│  • Initializes agent0 SDK with chain config                     │
└─────────────────────────────────────────────────────────────────┘
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
            ┌───────────┐ ┌──────────┐ ┌──────────────┐
            │ R2 Client │ │ agent0   │ │ Local        │
            │           │ │ SDK      │ │ Registry     │
            │ Upload    │ │          │ │              │
            │ JSON      │ │ On-chain │ │ Track IDs    │
            └───────────┘ │ register │ │              │
                          └──────────┘ └──────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   Ethereum Mainnet  │
                    │   ERC-8004 Registry │
                    └─────────────────────┘
```

## File Changes After Registration

### 1. `mesh/erc8004/registered_agents.json`

```json
{
  "sepolia": {
    "TokenResolverAgent": "11155111:413",
    "TrendingTokenAgent": "11155111:414",
    "TwitterIntelligenceAgent": "11155111:415"
  },
  "mainnet": {
    "TokenResolverAgent": "1:1",
    "TrendingTokenAgent": "1:2",
    "TwitterIntelligenceAgent": "1:3"
  }
}
```

### 2. R2: `erc8004/TokenResolverAgent.json`

The `registrations` array will contain both networks:

```json
{
  "registrations": [
    {
      "agentId": 413,
      "agentRegistry": "eip155:11155111:0x8004A818BFB912233c491871b3d84c89A494BD9e"
    },
    {
      "agentId": 1,
      "agentRegistry": "eip155:1:0xMAINNET_REGISTRY_ADDRESS"
    }
  ]
}
```

**Note:** The system automatically merges registrations from multiple chains - mainnet registration will preserve existing sepolia data.

## Known Limitations & Considerations

### 1. Multi-Chain Registrations

The system now properly merges registrations from multiple chains. When you register on mainnet:

- Existing sepolia registrations are preserved in the R2 JSON
- Each chain's registration is tracked separately in `registered_agents.json`
- The `registrations` array in R2 will contain entries for all chains

### 2. Gas Price Volatility

Mainnet gas prices fluctuate. The agent0 SDK handles gas estimation, but during high congestion:

- Transactions may take longer to confirm
- Consider using a higher priority fee if time-sensitive

### 3. Private Key Security

For mainnet deployment:

- Never commit private keys
- Consider using a hardware wallet or secure key management
- Use a dedicated deployment wallet, not your main wallet

## Rollback Plan

If something goes wrong:

1. **On-chain:** Agents can be deactivated via `agent.setActive(false)` but cannot be deleted
2. **R2:** Delete registration files: `r2_client.delete_registration("AgentName")`
3. **Local registry:** Edit `registered_agents.json` to remove entries

## Post-Deployment

After successful mainnet registration:

1. **Commit registry changes:**
   ```bash
   git add mesh/erc8004/registered_agents.json
   git commit -m "feat: register agents on mainnet"
   git push
   ```

2. **Verify metadata.json updates** after CI/CD runs

3. **Announce:** Update docs, social media, etc.

## Summary Checklist

- [ ] Receive mainnet registry contract address
- [ ] Update `mesh/erc8004/config.py` with mainnet address
- [ ] Set `ETH_RPC_URL` in environment
- [ ] Fund deployment wallet (~0.1 ETH recommended)
- [ ] Run dry-run: `uv run python -m mesh.erc8004.cli sync --chain mainnet --dry-run`
- [ ] Execute: `uv run python -m mesh.erc8004.cli sync --chain mainnet`
- [ ] Verify registrations on-chain and in R2
- [ ] Commit and push `registered_agents.json`
- [ ] Verify metadata.json is updated after CI/CD

## Quick Start (TL;DR)

```bash
# 1. Edit config.py - add mainnet registry address
vim mesh/erc8004/config.py

# 2. Set environment
export ETH_RPC_URL="https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY"
export ERC8004_PRIVATE_KEY="0x..."

# 3. Fund wallet with ~0.1 ETH

# 4. Preview
uv run python -m mesh.erc8004.cli sync --chain mainnet --dry-run

# 5. Deploy!
uv run python -m mesh.erc8004.cli sync --chain mainnet

# 6. Commit
git add mesh/erc8004/registered_agents.json
git commit -m "feat: register agents on mainnet"
git push
```
