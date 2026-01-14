# ERC-8004 Reputation System Roadmap

This document outlines the next steps for integrating the ERC-8004 Reputation Registry into Heurist Mesh.

## Current State (MVP)

The current implementation covers the **Identity Registry** only:
- Agents can be registered on-chain with MCP endpoints
- Registration files are stored on Cloudflare R2
- Support for Sepolia testnet (mainnet support planned)

## Reputation System Overview

The ERC-8004 Reputation Registry allows users to submit on-chain feedback for agents. This creates a decentralized trust layer where:

1. **Users** submit feedback (score 0-100, tags, optional text)
2. **Agent operators** can respond to feedback
3. **Clients** can query aggregate scores and filter by tags

### On-Chain Data Structure

```solidity
// Feedback entry
struct Feedback {
    uint8 score;           // 0-100
    string tag1;           // Primary tag (e.g., "accuracy", "speed")
    string tag2;           // Secondary tag
    string endpoint;       // Endpoint URL that was used
    string feedbackURI;    // IPFS/HTTP link to detailed feedback
    bytes32 feedbackHash;  // Hash of off-chain data
    bool isRevoked;        // Can be revoked by reviewer
}
```

## Implementation Plan

### Phase 1: Feedback Collection Infrastructure

**Goal**: Collect feedback from x402 payment completions

1. **Webhook Handler** (`mesh/erc8004/feedback_collector.py`)
   - Listen for successful x402 payment events
   - Automatically prompt users for feedback via UI/API
   - Store pending feedback in a queue

2. **Feedback API** (`mesh/erc8004/feedback_api.py`)
   - `POST /feedback` - Submit feedback for an agent
   - `GET /feedback/{agent_id}` - Get feedback summary
   - Rate limiting to prevent spam

3. **Feedback Data Model**
   ```python
   class FeedbackSubmission(TypedDict):
       agent_id: str           # ERC-8004 agent ID
       score: int              # 0-100
       tags: List[str]         # Up to 2 tags
       text: str | None        # Optional detailed feedback
       endpoint: str           # MCP endpoint used
       proof_of_payment: str   # x402 payment proof
   ```

### Phase 2: On-Chain Feedback Submission

**Goal**: Submit collected feedback to the Reputation Registry

1. **Batch Submitter** (`mesh/erc8004/reputation_submitter.py`)
   - Process feedback queue
   - Upload detailed feedback to R2 (feedbackURI)
   - Submit on-chain via `giveFeedback()`

2. **Cost Optimization**
   - Batch multiple feedbacks into single transactions
   - Use gas price thresholds
   - Consider L2 deployment for lower costs

3. **CLI Commands**
   ```bash
   uv run python -m mesh.erc8004.cli feedback submit --batch
   uv run python -m mesh.erc8004.cli feedback status <agent_id>
   ```

### Phase 3: Reputation Display

**Goal**: Surface reputation data in Mesh UI and agent discovery

1. **Reputation Fetcher** (`mesh/erc8004/reputation_reader.py`)
   - Query reputation summaries from subgraph
   - Cache results with TTL
   - Aggregate across multiple chains

2. **API Integration**
   - Add `reputation` field to agent metadata
   - Display scores in agent cards
   - Filter agents by minimum reputation

3. **Agent Metadata Extension**
   ```python
   class ReputationSummary(TypedDict):
       average_score: float      # 0-100
       total_reviews: int
       tags: Dict[str, int]      # tag -> count
       last_updated: int         # timestamp
   ```

### Phase 4: Response System

**Goal**: Allow agent operators to respond to feedback

1. **Response API**
   - `POST /feedback/{id}/response` - Submit response
   - Notify agent operators of new feedback

2. **On-Chain Responses**
   - Use `appendResponse()` for critical feedback
   - Store response text on R2

## Technical Considerations

### Gas Costs

Current Sepolia estimates (will vary on mainnet):
- `giveFeedback()`: ~100k gas
- `appendResponse()`: ~80k gas

Consider:
- Batching feedback submissions
- Using L2 for high-volume scenarios
- Subsidizing gas for early adopters

### Spam Prevention

1. **Proof of Payment**: Require x402 payment proof
2. **Rate Limiting**: Max N feedbacks per address per day
3. **Minimum Interaction**: Require actual agent usage

### Privacy

- Feedback text is off-chain (R2/IPFS)
- On-chain: only scores, tags, and hashes
- Option for anonymous feedback (with proof of payment)

## Environment Variables

Additional variables needed:

```bash
# Reputation System
REPUTATION_FEEDBACK_API_URL=https://mesh.heurist.xyz/feedback
REPUTATION_BATCH_SIZE=10
REPUTATION_GAS_THRESHOLD_GWEI=50
```

## Timeline

| Phase | Scope | Dependency |
|-------|-------|------------|
| Phase 1 | Feedback collection | x402 payment events |
| Phase 2 | On-chain submission | Phase 1 + gas budget |
| Phase 3 | UI integration | Phase 2 + frontend work |
| Phase 4 | Response system | Phase 3 |

## References

- [ERC-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004)
- [Agent0 SDK Documentation](https://github.com/erc-8004/agent0-py)
- [Reputation Registry Contract](https://sepolia.etherscan.io/address/0x8004B663056A597Dffe9eCcC1965A193B7388713)
