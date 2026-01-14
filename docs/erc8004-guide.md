## Background
The Agent-to-Agent (A2A) Protocol and ERC-8004 are two complementary standards that, together, form the foundational stack for a trustless, interoperable, and open economy of autonomous AI agents. A2A Protocol: An open-source standard (initiated by Google, now at the Linux Foundation) that acts as the communication layer. It is the "universal translator" that allows AI agents, built on different frameworks (like LangChain, Amazon Bedrock, etc.) and by different organizations, to understand each other and collaborate on tasks. ERC-8004: An Ethereum standard proposal that acts as the on-chain trust layer. It extends the A2A protocol by using the blockchain to provide verifiable identity, reputation, and validation. In simple terms: A2A lets agents talk to each other. ERC-8004 lets them trust each other enough to transact securely in an open, public environment. The A2A (Agent-to-Agent) Protocol The A2A protocol was designed to solve the "walled garden" problem for AI agents. Before its introduction, agents built by different vendors or on different platforms could not easily interoperate. Core Technical Components: Agent Card: A standardized JSON file that acts as an agent's "business card." It's published at an endpoint and describes the agent's identity, capabilities (skills), security requirements, and how to communicate with it. Task Lifecycle: A standardized set of states for any task an agent performs (e.g., submitted, working, input-required, completed, failed). This allows a "client" agent to reliably manage and track work being "outsourced" to a "remote" agent. Standardized Messaging: A defined protocol for messages and artifacts (the "work product," like a document or image). This ensures that when one agent sends a request, the other can correctly parse and process it, regardless of its internal architecture. The Inherent Limitation: The A2A protocol is primarily a communication standard. It works perfectly within trusted environments (like inside a single corporation) but lacks the native tools to solve for trust in a permissionless setting. It has no built-in way to prove: Are you who you say you are? (Identity) Are you any good at what you do? (Reputation) Did you actually do the work I paid for? (Validation) ERC-8004: The On-Chain Trust Layer This is where ERC-8004, as proposed on Ethereum Magicians, provides the critical Web3 extension. It anchors the A2A protocol's concepts to the Ethereum blockchain using three lightweight, on-chain registries. 1. Identity Registry What it is: A smart contract that registers agents and assigns them a unique, on-chain identity. Technical Implementation: It is an ERC-721 (NFT) contract. Each registered agent is minted a unique NFT. The agentId is the NFT's tokenId. This NFT acts as a permanent, non-forgeable "passport" for the agent. How it works: The tokenURI of the NFT points to the agent's registration file (its "Agent Card"). By storing this link on-chain, the agent's identity and capabilities are anchored to a verifiable, blockchain-based identifier. This makes the agent's identity composable and discoverable. 2. Reputation Registry What it is: A standard interface for clients to submit feedback about an agent's performance, creating a permanent, auditable on-chain record. Technical Implementation: A smart contract with a core function like giveFeedback. How it works: To save gas and maintain flexibility, the registry only stores minimal data on-chain: typically a numerical score (e.g., 0-100), filterable on-chain tags, and a fileURI (e.g., an IPFS hash). The fileURI points to a more detailed, off-chain JSON file containing qualitative feedback or other complex data. This "thin" on-chain data is still highly composable, allowing other smart contracts to perform basic checks (e.g., require agent.reputation > 90). 3. Validation Registry What it is: The most critical component for trustless transactions. It's a standard interface for agents to prove they completed a task correctly. Technical Implementation: A contract that allows a server agent to requestValidation and a validator to submitValidationResponse. How it works: An agent completes a task and submits a hash of its results. An independent, third-party validator (or system) checks the work. This validation can use various methods: Crypto-economic: A validator stakes assets to vouch for the result (e.g., via an Actively Validated Service on EigenLayer). Cryptographic: A zero-knowledge proof (zk-proof) or a Trusted Execution Environment (TEE) attestation is provided as proof. The validator posts a verified (true/false) status to the registry. This on-chain boolean is the "green light" that other smart contracts can use to automatically trigger actions, such as releasing payment from an escrow. The Full Stack: A2A + ERC-8004 Workflow Discover (Identity): An agent (Agent A) needs a task done. It queries the ERC-8004 Identity Registry to find agents with the required skill. Trust (Reputation): Agent A filters the results by querying the ERC-8004 Reputation Registry to find a high-quality agent (Agent B). Hire (A2A): Agent A initiates a task with Agent B using the standard A2A protocol messaging. Work (A2A): Agent B performs the task and communicates its progress using the A2A task lifecycle. Prove (Validation): Agent B submits its final work to the ERC-8004 Validation Registry to be verified. Pay (On-Chain): An escrow smart contract (which is not part of the ERC but works with it) programmatically reads the Validation Registry. Upon seeing a verified = true status, it automatically releases payment to Agent B. Review (Reputation): Agent A calls giveFeedback on the Reputation Registry to rate Agent B's performance, contributing to its on-chain history.

## Advisor Recommendations (need review)
Here’s how I’d wire Heurist Mesh into ERC‑8004 in a way that (a) is realistic to ship and (b) sets you up as “agent infra” for everyone else.

1. Mental model: how Mesh, MCP, x402, and ERC‑8004 line up

From the spec + Agent0 SDK docs, ERC‑8004 gives you:

Identity Registry – ERC‑721 “AgentIdentity (AID)” NFT on Sepolia (chainId 11155111, contract 0x8004…8847) where tokenURI points at an agent registration file (that JSON with type, name, description, endpoints, etc.).

2. Reputation Registry – giveFeedback() etc. with a thin on‑chain score and off‑chain JSON file.

3. Validation Registry – standard hooks for “I did a job, someone validated it”, with a boolean + optional extra data.

Agent0 SDK is basically the batteries‑included toolkit for this: it can create agents, set MCP/A2A endpoints, set trust flags, and register via IPFS or HTTP. You must use it by following the README.md of /home/appuser/agent0-py (remember, we use uv to manage python)

Heurist Mesh already gives you: (read heurist-agent-framework/docs/mesh-agent-system.md for the details)

Runtime & business logic – MeshAgent subclasses and the Mesh HTTP API (/mesh_request).

MCP surface – heurist-mesh-mcp-server + MCP Portal that spins up MCP servers backed by Mesh agents.

example MCP URL: https://mesh.heurist.xyz/mcp/agents/YahooFinanceAgent (this contains all tools under YahooFinanceAgent) every agent has such one URL

x402 surface – the dynamic Express routes (/x402/agents/{agentId}/{toolName}) protected by paymentMiddleware and backed by callMeshTool.

example x402 URL: https://mesh.heurist.xyz/x402/agents/AIXBTProjectInfoAgent/search_projects (USDC payment on Base chain) and https://mesh.heurist.xyz/x402/solana/agents/AIXBTProjectInfoAgent/search_projects (USDC payment on Solana)

every tool of every x402-enabled agent has two x402 URLs (one for base another for solana)

So, for the rest of the world, an “ERC‑8004‑compatible Heurist agent” is just:

A Mesh agent that has:
– a stable MCP endpoint (and optionally A2A),
– an on‑chain identity in the 8004 Identity Registry,
– and a registration JSON that ties those together.

2. What should a “Heurist Mesh ERC‑8004 agent” look like?

Per the EIP, a valid registration file MUST look roughly like this:
{
  "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  "name": "MyHeuristAgent",
  "description": "Natural-language description of what this agent does...",
  "image": "https://mesh.heurist.ai/images/my-agent.png",
  "endpoints": [
    {
      "name": "MCP",
      "endpoint": "https://mcp.heurist.ai/sse/my-heurist-agent",
      "version": "2025-06-18"
    },
    {
      "name": "agentWallet",
      "endpoint": "eip155:8453:0x7d9d1821d15B9e0b8Ab98A058361233E255E405D"
    }
  ],
  "registrations": [
    {
      "agentId": 123,
      "agentRegistry": "eip155:11155111:0x8004a6090Cd10A7288092483047B097295Fb8847"
    }
  ],
  "supportedTrust": [
    "reputation",
    "crypto-economic"
  ],
  "active": true,
  "x402support": true,
  "metadata": {
    "x402Endpoints": {
      "version": "v1",
      "tools": {
        "search_projects": {
          "base": "https://x402.heurist.xyz/x402/agents/MyHeuristAgent/search_projects",
          "solana": "https://x402.heurist.xyz/x402/solana/agents/MyHeuristAgent/search_projects"
        }
      }
    }
  }
}


Notes:

The spec uses supportedTrust (singular), not supportedTrusts. Your sample JSON is otherwise sane, just tweak that key.

active and x402support are not in the core EIP, but Agent0 uses them and exposes agent.active / agent.x402support and search filters for them, so they’re good optional fields to keep. Agent0 only accepts endpoint names from its EndpointType enum, so x402 URLs belong under metadata (x402Endpoints) instead of endpoints. Use per-tool entries (one tool → base + solana URLs) under metadata.x402Endpoints.tools.

agentId is the tokenId in the Identity Registry. You don’t set this manually; it’s filled in once you register via agent.registerIPFS() or agent.register().

The minimum viable Heurist → ERC‑8004 mapping per agent is:

name ← MeshAgent.metadata["name"]

description ← MeshAgent.metadata["description"] + one sentence like “This tool is created and maintained by Heurist.”

image ← MeshAgent.metadata["image_url"]

agentWallet endpoint ← either metadata["author_address"] or your central HEURIST_PAY_TO wallet.

MCP endpoint ← an SSE MCP server that exposes this agent’s tools.

x402 endpoints ← per-tool base/solana URLs under metadata.x402Endpoints, using the agent class name.

Everything else (OASF skills, extra endpoints, ENS, DID, etc.) is additive later.

3. Where should ERC‑8004 metadata live in heurist-agent-framework?

You already have a nice metadata blob on each MeshAgent.

I’d extend this (non‑breaking) with an erc8004 sub‑object:
self.metadata["erc8004"] = {
    "enabled": False,               # opt-in for ERC‑8004
    "chain_id": 11155111,           # Sepolia by default
    "identity_registry": "0x8004a6090Cd10A7288092483047B097295Fb8847",
    # reputation / validation registries – fill when stable
    "reputation_registry": None,
    "validation_registry": None,
    # trust models this agent wants to advertise
    "supported_trust": ["reputation", "crypto-economic"],
    # wallet that should receive payments / represent the agent on-chain
    "wallet_chain_id": 8453,        # Base, if you want
    "wallet_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
    # optional OASF tags for discovery
    "skills": [],
    "domains": [],
    # optional override for display name / description / image if needed
    "display_name": None,
    "display_description": None,
    "image_override": None,
}

This gives you:

A single source of truth for “should this Mesh agent show up in ERC‑8004?”

Enough information for a central registration script to do the right thing.

A place to stuff OASF skills/domains once you’re ready to use Agent0’s taxonomy helpers.

You don’t need to change any runtime behavior; this is just config.

4. Registration & update flow using agent0-sdk
4.1. Initialize the SDK (one time per environment)
from agent0_sdk import SDK
import os

sdk = SDK(
    chainId=11155111,                # Sepolia
    rpcUrl=os.getenv("SEPOLIA_RPC_URL"),
    signer=os.getenv("PRIVATE_KEY"), # wallet that will own agent NFTs
    ipfs="pinata",                   # or "filecoinPin" or "node"
    pinataJwt=os.getenv("PINATA_JWT")
)


Agent0 defaults to the Sepolia Identity / Reputation registry addresses for that chainId.

4.2. A sync script inside Heurist Mesh

Create a Python script in the Mesh backend (or a standalone job) that:

Discovers eligible agents

Use your existing AgentLoader to instantiate all MeshAgent subclasses and read metadata.

Filters erc8004.enabled == True

For each agent: build a “desired state” representation

Something like:

def build_desired_registration(mesh_agent) -> dict:
    m = mesh_agent.metadata
    e = m.get("erc8004", {})

    name = e.get("display_name") or m["name"]
    description = e.get("display_description") or m["description"]
    image = e.get("image_override") or m.get("image_url")

    agent_class = mesh_agent.__class__.__name__

    # MCP endpoint – see section 5 below
    mcp_endpoint = f"https://mcp.heurist.ai/sse/agents/{agent_class}"

    # x402 endpoints – one per tool, base + solana
    x402_endpoints = {
        "version": "v1",
        "tools": {
            tool["function"]["name"]: {
                "base": f"https://x402.heurist.xyz/x402/agents/{agent_class}/{tool['function']['name']}",
                "solana": f"https://x402.heurist.xyz/x402/solana/agents/{agent_class}/{tool['function']['name']}",
            }
            for tool in mesh_agent.get_tool_schemas()
        },
    }

    supported_trust = e.get("supported_trust", ["reputation"])

    return {
        "name": name,
        "description": description,
        "image": image,
        "mcp_endpoint": mcp_endpoint,
        "x402_endpoints": x402_endpoints,
        "wallet_address": e.get("wallet_address") or m.get("author_address"),
        "wallet_chain_id": e.get("wallet_chain_id", 8453),
        "supported_trust": supported_trust,
        "skills": e.get("skills", []),
        "domains": e.get("domains", []),
    }


Reconcile with existing ERC‑8004 agent (if any)

You can stash the minted Agent0 ID ("11155111:123") into Mesh metadata or a sidecar DB the first time you register.

If you have it, load via:
agent = sdk.loadAgent("11155111:123")

Otherwise, you can search by name / custom metadata, but better to store the ID once.

5. Create or update the Agent0 object

Creation:
desired = build_desired_registration(mesh_agent)

agent = sdk.createAgent(
    name=desired["name"],
    description=desired["description"],
    image=desired["image"],
)

# Endpoints
agent.setMCP(desired["mcp_endpoint"])
# optional: set A2A later, see section 5
# agent.setA2A(f"https://mesh.heurist.ai/a2a/{mesh_agent.metadata['name']}.json")

# Wallet + trust
agent.setAgentWallet(
    desired["wallet_address"],
    chainId=desired["wallet_chain_id"],
)
agent.setTrust(
    reputation="reputation" in desired["supported_trust"],
    cryptoEconomic="crypto-economic" in desired["supported_trust"]
)

# Metadata / status
agent.setMetadata({
    "meshAgentId": mesh_agent.metadata["name"],
    "source": "Heurist Mesh",
    "version": mesh_agent.metadata.get("version", "1.0.0"),
})
agent.setActive(True)
# If you want Agent0 search to show this as x402-capable:
agent.setMetadata({"x402support": True})


Update (e.g., new description):
# Load existing agent
agent = sdk.loadAgent(stored_agent_id)

desired = build_desired_registration(mesh_agent)

agent.updateInfo(
    name=desired["name"],
    description=desired["description"],
    image=desired["image"],
)
agent.setMCP(desired["mcp_endpoint"])
agent.setAgentWallet(
    desired["wallet_address"],
    chainId=desired["wallet_chain_id"],
)
# …update trust / metadata if needed
6. egister / re‑register

When you call registerIPFS():

If the agent isn’t minted yet, Agent0 will:

upload the registration JSON to IPFS,

call IdentityRegistry.register(tokenURI) on 0x8004…8847,

emit an AgentIdentity NFT and return agent.agentId.

If it is minted, it will just update tokenURI to the new IPFS hash.

agent.registerIPFS()
print("Registered agent:", agent.agentId, "URI:", agent.agentURI)

Answering “how do I update agent description?”

For your concrete question: you don’t need a new NFT; just:

Change the description in heurist-agent-framework (metadata["description"]).

Run the sync script.

For each ERC‑8004‑enabled agent:

agent = sdk.loadAgent("11155111:123")
agent.updateInfo(description=new_description)
agent.registerIPFS()  # updates tokenURI only


Agent0 hides the details of calling _setTokenURI() on the registry for you.

Immediate priorities (v0)

Add erc8004 metadata to MeshAgent base class.

Pick 3–5 flagship agents (e.g., CoingeckoTokenInfoAgent, ElfaTwitterIntelligenceAgent, ExaSearchAgent) to pilot.

Decide MCP endpoint strategy:

quick: single shared MCP endpoint,

ideal: one endpoint per agent (via MCP Portal or extended heurist-mesh-mcp-server).

Implement registration sync job using agent0-sdk + Sepolia registry.

Verify in 8004scan that identities show up with correct endpoints & metadata.
