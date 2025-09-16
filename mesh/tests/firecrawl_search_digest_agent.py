import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.firecrawl_search_digest_agent import FirecrawlSearchDigestAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "natural_language_query_with_analysis": {
        "input": {
            "query": "What are the most recent developments in decentralized AI and blockchain integration?",
            "raw_data_only": False,
        },
        "description": "Natural language query with AI analysis for decentralized AI and blockchain",
    },
    "natural_language_query_raw_data": {
        "input": {
            "query": "What are the most recent developments in decentralized AI and blockchain integration?",
            "raw_data_only": True,
        },
        "description": "Natural language query with raw data only for decentralized AI and blockchain",
    },
    "web_search_with_time_filter": {
        "input": {
            "tool": "firecrawl_web_search",
            "tool_arguments": {"search_term": "Ethereum scaling solutions", "time_filter": "qdr:w", "limit": 5},
        },
        "description": "Direct web search with time filtering (past week) for Ethereum scaling",
    },
    "web_search_site_specific": {
        "input": {
            "tool": "firecrawl_web_search",
            "tool_arguments": {"search_term": "site:coindesk.com bitcoin news", "limit": 5},
        },
        "description": "Site-specific search using site: operator for CoinDesk bitcoin news",
    },
    "web_search_with_or_operator": {
        "input": {
            "tool": "firecrawl_web_search",
            "tool_arguments": {
                "search_term": "bitcoin OR ethereum price prediction",
                "time_filter": "qdr:d",
                "limit": 6,
            },
        },
        "description": "Search with OR operator and daily time filter for price predictions",
    },
    "extract_web_data_multiple_urls": {
        "input": {
            "tool": "firecrawl_extract_web_data",
            "tool_arguments": {
                "urls": ["https://ethereum.org/en/roadmap/", "https://ethereum.org/en/developers/"],
                "extraction_prompt": "Extract information about Ethereum's development roadmap, upcoming features, and developer resources. Focus on technical improvements and timeline information.",
            },
        },
        "description": "Data extraction from multiple Ethereum.org URLs with specific prompt",
    },
    "extract_web_data_wildcard": {
        "input": {
            "tool": "firecrawl_extract_web_data",
            "tool_arguments": {
                "urls": ["blog.ethereum.org/*"],
                "extraction_prompt": "Extract recent blog posts about Ethereum updates, technical improvements, and community announcements. Include titles, dates, and key points.",
            },
        },
        "description": "Data extraction using wildcard pattern for Ethereum blog posts",
    },
    "scrape_url_default": {
        "input": {
            "tool": "firecrawl_scrape_url",
            "tool_arguments": {
                "url": "https://vitalik.ca/",
            },
        },
        "description": "URL scraping with default wait time for Vitalik's website",
    },
    "scrape_url_custom_wait": {
        "input": {
            "tool": "firecrawl_scrape_url",
            "tool_arguments": {
                "url": "https://blog.ethereum.org/",
                "wait_time": 8000,
            },
        },
        "description": "URL scraping with custom wait time for Ethereum blog",
    },
    "time_sensitive_natural_query": {
        "input": {
            "query": "Find today's news about crypto market trends and major developments",
            "raw_data_only": False,
        },
        "description": "Time-sensitive natural language query for today's crypto news",
    },
    "blockchain_projects_research": {
        "input": {
            "query": "Research the latest developments in Layer 2 scaling solutions like Polygon, Arbitrum, and Optimism",
            "raw_data_only": False,
        },
        "description": "Research query about specific Layer 2 blockchain projects",
    },
    "complex_search_multiple_operators": {
        "input": {
            "tool": "firecrawl_web_search",
            "tool_arguments": {
                "search_term": '"zero knowledge proofs" AND ("zkSync" OR "Polygon") site:medium.com',
                "time_filter": "qdr:m",
                "limit": 8,
            },
        },
        "description": "Complex search with multiple operators and filters for zero knowledge proofs",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(FirecrawlSearchDigestAgent, TEST_CASES))
