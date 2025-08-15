import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.firecrawl_search_digest_agent import FirecrawlSearchDigestAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = FirecrawlSearchDigestAgent()
    try:
        # Test 1: Natural language query with AI analysis
        agent_input_query = {
            "query": "What are the most recent developments in decentralized AI and blockchain integration?",
            "raw_data_only": False,
        }
        agent_output_query = await agent.handle_message(agent_input_query)

        # Test 2: Natural language query with raw data only
        agent_input_query_raw = {
            "query": "What are the most recent developments in decentralized AI and blockchain integration?",
            "raw_data_only": True,
        }
        agent_output_query_raw = await agent.handle_message(agent_input_query_raw)

        # Test 3: Direct web search with time filter (past week)
        agent_input_search_recent = {
            "tool": "firecrawl_web_search",
            "tool_arguments": {
                "search_term": "Ethereum scaling solutions",
                "time_filter": "qdr:w",
                "limit": 5
            },
        }
        agent_output_search_recent = await agent.handle_message(agent_input_search_recent)

        # Test 4: Direct web search with site-specific operator
        agent_input_search_site = {
            "tool": "firecrawl_web_search",
            "tool_arguments": {
                "search_term": "site:coindesk.com bitcoin news",
                "limit": 5
            },
        }
        agent_output_search_site = await agent.handle_message(agent_input_search_site)

        # Test 5: Direct web search with OR operator
        agent_input_search_or = {
            "tool": "firecrawl_web_search",
            "tool_arguments": {
                "search_term": "bitcoin OR ethereum price prediction",
                "time_filter": "qdr:d",
                "limit": 6
            },
        }
        agent_output_search_or = await agent.handle_message(agent_input_search_or)

        # Test 6: Extract web data with specific prompt
        agent_input_extract = {
            "tool": "firecrawl_extract_web_data",
            "tool_arguments": {
                "urls": ["https://ethereum.org/en/roadmap/", "https://ethereum.org/en/developers/"],
                "extraction_prompt": "Extract information about Ethereum's development roadmap, upcoming features, and developer resources. Focus on technical improvements and timeline information.",
            },
        }
        agent_output_extract = await agent.handle_message(agent_input_extract)

        # Test 7: Extract web data with wildcard pattern
        agent_input_extract_wildcard = {
            "tool": "firecrawl_extract_web_data",
            "tool_arguments": {
                "urls": ["blog.ethereum.org/*"],
                "extraction_prompt": "Extract recent blog posts about Ethereum updates, technical improvements, and community announcements. Include titles, dates, and key points.",
            },
        }
        agent_output_extract_wildcard = await agent.handle_message(agent_input_extract_wildcard)

        # Test 8: Scrape specific URL with default wait time
        agent_input_scrape = {
            "tool": "firecrawl_scrape_url",
            "tool_arguments": {
                "url": "https://vitalik.ca/",
            },
        }
        agent_output_scrape = await agent.handle_message(agent_input_scrape)

        # Test 9: Scrape specific URL with custom wait time
        agent_input_scrape_custom_wait = {
            "tool": "firecrawl_scrape_url",
            "tool_arguments": {
                "url": "https://blog.ethereum.org/",
                "wait_time": 8000,
            },
        }
        agent_output_scrape_custom_wait = await agent.handle_message(agent_input_scrape_custom_wait)

        # Test 10: Natural language query for time-sensitive search
        agent_input_time_sensitive = {
            "query": "Find today's news about crypto market trends and major developments",
            "raw_data_only": False,
        }
        agent_output_time_sensitive = await agent.handle_message(agent_input_time_sensitive)

        # Test 11: Natural language query about specific blockchain projects
        agent_input_blockchain_projects = {
            "query": "Research the latest developments in Layer 2 scaling solutions like Polygon, Arbitrum, and Optimism",
            "raw_data_only": False,
        }
        agent_output_blockchain_projects = await agent.handle_message(agent_input_blockchain_projects)

        # Test 12: Complex search with multiple operators
        agent_input_complex_search = {
            "tool": "firecrawl_web_search",
            "tool_arguments": {
                "search_term": "\"zero knowledge proofs\" AND (\"zkSync\" OR \"Polygon\") site:medium.com",
                "time_filter": "qdr:m",
                "limit": 8
            },
        }
        agent_output_complex_search = await agent.handle_message(agent_input_complex_search)

        # Save results to YAML file
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "natural_language_query_with_analysis": {
                "description": "Test natural language query processing with AI analysis",
                "input": agent_input_query,
                "output": agent_output_query
            },
            "natural_language_query_raw_data": {
                "description": "Test natural language query with raw data only",
                "input": agent_input_query_raw,
                "output": agent_output_query_raw
            },
            "web_search_with_time_filter": {
                "description": "Test direct web search with time filtering (past week)",
                "input": agent_input_search_recent,
                "output": agent_output_search_recent
            },
            "web_search_site_specific": {
                "description": "Test site-specific search using site: operator",
                "input": agent_input_search_site,
                "output": agent_output_search_site
            },
            "web_search_with_or_operator": {
                "description": "Test search with OR operator and time filter",
                "input": agent_input_search_or,
                "output": agent_output_search_or
            },
            "extract_web_data_multiple_urls": {
                "description": "Test data extraction from multiple specific URLs",
                "input": agent_input_extract,
                "output": agent_output_extract
            },
            "extract_web_data_wildcard": {
                "description": "Test data extraction using wildcard pattern",
                "input": agent_input_extract_wildcard,
                "output": agent_output_extract_wildcard
            },
            "scrape_url_default": {
                "description": "Test URL scraping with default wait time",
                "input": agent_input_scrape,
                "output": agent_output_scrape
            },
            "scrape_url_custom_wait": {
                "description": "Test URL scraping with custom wait time",
                "input": agent_input_scrape_custom_wait,
                "output": agent_output_scrape_custom_wait
            },
            "time_sensitive_natural_query": {
                "description": "Test time-sensitive natural language query",
                "input": agent_input_time_sensitive,
                "output": agent_output_time_sensitive
            },
            "blockchain_projects_research": {
                "description": "Test research query about specific blockchain projects",
                "input": agent_input_blockchain_projects,
                "output": agent_output_blockchain_projects
            },
            "complex_search_multiple_operators": {
                "description": "Test complex search with multiple operators and filters",
                "input": agent_input_complex_search,
                "output": agent_output_complex_search
            },
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False, width=120)

        print(f"Results saved to {output_file}")
        print(f"Executed {len(yaml_content)} test scenarios successfully!")

        # Print summary of test scenarios
        print("\nTest Scenarios Executed:")
        for i, (key, value) in enumerate(yaml_content.items(), 1):
            print(f"{i:2}. {key}: {value['description']}")

    except Exception as e:
        print(f"Error during agent execution: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await agent.cleanup()


if __name__ == "__main__":
    try:
        asyncio.run(run_agent())
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")