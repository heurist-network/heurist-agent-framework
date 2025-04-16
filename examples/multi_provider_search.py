import asyncio
import os

from dotenv import load_dotenv

from core.clients.search_client import SearchClient
from core.llm import LLMProvider
from core.workflows.deep_research import ResearchWorkflow

# Load environment variables
load_dotenv()


async def main():
    """
    Example script demonstrating the ResearchWorkflow with multiple search providers.
    This shows how using multiple providers can improve research quality and parallelization.
    """
    # Initialize LLM provider
    llm_provider = LLMProvider(
        base_url=os.environ.get("LLM_BASE_URL"),
        api_key=os.environ.get("LLM_API_KEY"),
        model_id=os.environ.get("LLM_MODEL_ID", "gpt-4"),
    )

    # Initialize search clients for different providers
    search_clients = {
        # Exa search client (requires API key)
        "exa": SearchClient(client_type="exa", api_key=os.environ.get("EXA_API_KEY", ""), rate_limit=0)
        if os.environ.get("EXA_API_KEY")
        else None,
        # Firecrawl search client (requires API key)
        "firecrawl": SearchClient(
            client_type="firecrawl", api_key=os.environ.get("FIRECRAWL_API_KEY", ""), rate_limit=0
        )
        if os.environ.get("FIRECRAWL_API_KEY")
        else None,
        # DuckDuckGo search client (no API key required - always available)
        "duckduckgo": SearchClient(client_type="duckduckgo", rate_limit=0),
    }

    # Remove None values (clients with missing API keys)
    search_clients = {k: v for k, v in search_clients.items() if v is not None}

    # Initialize the research workflow with multiple search clients
    workflow = ResearchWorkflow(
        llm_provider=llm_provider,
        tool_manager=None,  # Not needed for this example
        search_clients=search_clients,
    )

    # Run a research task using all available providers in parallel
    research_question = "What are the health benefits of intermittent fasting?"

    print(f"Researching: {research_question}")
    print(f"Using search providers: {', '.join(search_clients.keys())}")

    report, _, result = await workflow.process(
        message=research_question,
        workflow_options={
            "breadth": 3,  # Number of search queries to generate
            "depth": 1,  # Depth of research recursion
            "concurrency": 10,  # Maximum concurrent requests
            "multi_provider": True,  # Use multiple providers (automatically enabled)
            "raw_data_only": False,  # Generate a formatted report
        },
    )

    print("\n=== Research Summary ===")
    print(f"Total sources found: {len(result['visited_urls'])}")
    print(f"Total learnings: {len(result['learnings'])}")

    print("\n=== Report ===")
    print(report)

    # Display the first few learnings
    print("\n=== Sample Learnings ===")
    for i, learning in enumerate(result["learnings"][:5]):
        print(f"{i + 1}. {learning}")

    # Display the sources
    print("\n=== Sources ===")
    for i, url in enumerate(result["visited_urls"][:5]):
        print(f"{i + 1}. {url}")


if __name__ == "__main__":
    asyncio.run(main())
