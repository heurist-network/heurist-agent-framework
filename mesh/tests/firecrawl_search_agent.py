import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.firecrawl_search_agent import FirecrawlSearchAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "natural_language_query_with_analysis": {
        "input": {
            "query": "What are the latest developments in zero knowledge proofs?",
            "raw_data_only": False,
        },
        "description": "Natural language query with AI analysis for zero knowledge proofs",
    },
    "natural_language_query_raw_data": {
        "input": {
            "query": "What are the latest developments in zero knowledge proofs?",
            "raw_data_only": True,
        },
        "description": "Natural language query with raw data only for zero knowledge proofs",
    },
    "direct_search": {
        "input": {
            "tool": "firecrawl_web_search",
            "tool_arguments": {"search_term": "zero knowledge proofs recent advancements"},
        },
        "description": "Direct tool call for web search about zero knowledge proofs",
    },
    "direct_extract": {
        "input": {
            "tool": "firecrawl_extract_web_data",
            "tool_arguments": {
                "urls": ["https://ethereum.org/en/zero-knowledge-proofs/"],
                "extraction_prompt": "Extract information about how zero knowledge proofs are being used in blockchain technology",
                "enable_web_search": False,
            },
        },
        "description": "Direct tool call to extract web data from Ethereum.org about zero knowledge proofs",
    },
    "scrape_heurist_homepage": {
        "input": {
            "query": "Scap me data of heurist.ai and generate a response about their services and offerings",
            "raw_data_only": False,
        },
        "description": "Scrape Heurist.ai homepage and generate response about services",
    },
    "heurist_services_query": {
        "input": {
            "query": "What services and products does Heurist.ai offer? What makes them unique in the AI space?",
            "raw_data_only": False,
        },
        "description": "Natural language query about Heurist services and uniqueness in AI space",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(FirecrawlSearchAgent, TEST_CASES))
