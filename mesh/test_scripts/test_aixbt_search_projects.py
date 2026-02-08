"""
Test script for AIXBTProjectInfoAgent search_projects method

This script tests various search scenarios for the AIXBT API including:
- Search by name, ticker, Twitter handle
- Filter by blockchain (Ethereum, Solana, Base)
- Filter by score (trending projects)
- Limit parameter testing
- Error handling

Prerequisites:
    1. Set AIXBT_API_KEY environment variable in your .env file
    2. Run with: uv run python mesh/test_scripts/test_aixbt_search_projects.py

Test Coverage:
    - Search by project name
    - Search by ticker symbol
    - Search by Twitter handle
    - Filter by blockchain network
    - Get trending projects (high scores)
    - Ecosystem-specific queries (Solana, Base)
    - Full project details structure
    - Error handling
    - Limit parameter validation
"""

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import asyncio
import json
from mesh.agents.aixbt_project_info_agent import AIXBTProjectInfoAgent


async def test_search_by_name():
    """Test searching projects by name"""
    print("\n" + "="*60)
    print("TEST 1: Search by Name - 'Heurist'")
    print("="*60)
    async with AIXBTProjectInfoAgent() as agent:
        result = await agent.search_projects(name="Heurist", limit=5)
        print(f"Found {len(result.get('projects', []))} projects")
        if result.get('projects'):
            for project in result['projects']:
                print(f"  - {project.get('name')} ({project.get('ticker', 'N/A')})")
                print(f"    Twitter: @{project.get('xHandle', 'N/A')}")
                print(f"    Score: {project.get('score', 'N/A')}")
        print(f"\nFull response:\n{json.dumps(result, indent=2)}")


async def test_search_by_ticker():
    """Test searching projects by ticker symbol"""
    print("\n" + "="*60)
    print("TEST 2: Search by Ticker - 'ETH'")
    print("="*60)
    async with AIXBTProjectInfoAgent() as agent:
        result = await agent.search_projects(ticker="ETH", limit=5)
        print(f"Found {len(result.get('projects', []))} projects")
        if result.get('projects'):
            for project in result['projects']:
                print(f"  - {project.get('name')} ({project.get('ticker', 'N/A')})")
        print(f"\nFull response:\n{json.dumps(result, indent=2)}")


async def test_search_by_twitter():
    """Test searching projects by Twitter handle"""
    print("\n" + "="*60)
    print("TEST 3: Search by Twitter Handle - '@heurist_ai'")
    print("="*60)
    async with AIXBTProjectInfoAgent() as agent:
        result = await agent.search_projects(xHandle="@heurist_ai", limit=5)
        print(f"Found {len(result.get('projects', []))} projects")
        if result.get('projects'):
            for project in result['projects']:
                print(f"  - {project.get('name')} ({project.get('ticker', 'N/A')})")
                print(f"    Twitter: @{project.get('xHandle', 'N/A')}")
        print(f"\nFull response:\n{json.dumps(result, indent=2)}")


async def test_search_by_chain():
    """Test searching projects by blockchain"""
    print("\n" + "="*60)
    print("TEST 4: Search by Chain - 'ethereum' with minScore 0.3")
    print("="*60)
    async with AIXBTProjectInfoAgent() as agent:
        result = await agent.search_projects(chain="ethereum", minScore=0.3, limit=10)
        print(f"Found {len(result.get('projects', []))} projects")
        if result.get('projects'):
            for project in result['projects'][:5]:  # Show first 5
                print(f"  - {project.get('name')} ({project.get('ticker', 'N/A')})")
                print(f"    Score: {project.get('score', 'N/A')}")
                contracts = project.get('contracts', [])
                eth_contracts = [c for c in contracts if c.get('chain') == 'ethereum']
                if eth_contracts:
                    print(f"    Contract: {eth_contracts[0].get('address', 'N/A')}")
        print(f"\nShowing first 5 of {len(result.get('projects', []))} projects")


async def test_trending_projects():
    """Test getting trending projects with high score threshold"""
    print("\n" + "="*60)
    print("TEST 5: Trending Projects - minScore 0.4")
    print("="*60)
    async with AIXBTProjectInfoAgent() as agent:
        result = await agent.search_projects(minScore=0.4, limit=15)
        print(f"Found {len(result.get('projects', []))} trending projects")
        if result.get('projects'):
            for i, project in enumerate(result['projects'], 1):
                print(f"{i}. {project.get('name')} ({project.get('ticker', 'N/A')}) - Score: {project.get('score', 'N/A')}")


async def test_solana_projects():
    """Test searching Solana ecosystem projects"""
    print("\n" + "="*60)
    print("TEST 6: Solana Ecosystem Projects - minScore 0.2")
    print("="*60)
    async with AIXBTProjectInfoAgent() as agent:
        result = await agent.search_projects(chain="solana", minScore=0.2, limit=10)
        print(f"Found {len(result.get('projects', []))} Solana projects")
        if result.get('projects'):
            for project in result['projects']:
                print(f"  - {project.get('name')} ({project.get('ticker', 'N/A')}) - Score: {project.get('score', 'N/A')}")


async def test_base_chain_projects():
    """Test searching Base chain projects"""
    print("\n" + "="*60)
    print("TEST 7: Base Chain Projects - minScore 0.2")
    print("="*60)
    async with AIXBTProjectInfoAgent() as agent:
        result = await agent.search_projects(chain="base", minScore=0.2, limit=10)
        print(f"Found {len(result.get('projects', []))} Base chain projects")
        if result.get('projects'):
            for project in result['projects']:
                print(f"  - {project.get('name')} ({project.get('ticker', 'N/A')}) - Score: {project.get('score', 'N/A')}")


async def test_project_details():
    """Test fetching detailed project information"""
    print("\n" + "="*60)
    print("TEST 8: Project Details - Full data structure for 'Bitcoin'")
    print("="*60)
    async with AIXBTProjectInfoAgent() as agent:
        result = await agent.search_projects(name="Bitcoin", limit=1)
        if result.get('projects') and len(result['projects']) > 0:
            project = result['projects'][0]
            print(f"Project: {project.get('name')}")
            print(f"Ticker: {project.get('ticker')}")
            print(f"Description: {project.get('description', 'N/A')[:200]}...")
            print(f"Score: {project.get('score')}")
            print(f"Twitter: @{project.get('xHandle')}")
            print(f"CoinGecko ID: {project.get('coingecko_id', 'N/A')}")

            print("\nContracts:")
            for contract in project.get('contracts', [])[:3]:
                print(f"  - {contract.get('chain')}: {contract.get('address')}")

            print("\nRecent Signals:")
            for signal in project.get('summaries', [])[:3]:
                print(f"  - [{signal.get('date', 'N/A')}] {signal.get('content', 'N/A')[:100]}...")

            print(f"\nFull JSON (first project):\n{json.dumps(project, indent=2)[:1000]}...")


async def test_error_handling():
    """Test error handling with invalid parameters"""
    print("\n" + "="*60)
    print("TEST 9: Error Handling - Non-existent project")
    print("="*60)
    async with AIXBTProjectInfoAgent() as agent:
        result = await agent.search_projects(name="ThisProjectDefinitelyDoesNotExist123456", limit=5)
        print(f"Found {len(result.get('projects', []))} projects")
        if result.get('error'):
            print(f"Error: {result['error']}")
        elif len(result.get('projects', [])) == 0:
            print("No projects found (expected)")


async def test_limit_parameter():
    """Test the limit parameter"""
    print("\n" + "="*60)
    print("TEST 10: Limit Parameter - Request 3 vs 20 trending projects")
    print("="*60)
    async with AIXBTProjectInfoAgent() as agent:
        result_small = await agent.search_projects(minScore=0.1, limit=3)
        result_large = await agent.search_projects(minScore=0.1, limit=20)

        print(f"With limit=3: Found {len(result_small.get('projects', []))} projects")
        print(f"With limit=20: Found {len(result_large.get('projects', []))} projects")


async def run_all_tests():
    """Run all test cases"""
    print("\n" + "#"*60)
    print("# AIXBT Project Info Agent - Search Method Tests")
    print("#"*60)

    tests = [
        test_search_by_name,
        test_search_by_ticker,
        test_search_by_twitter,
        test_search_by_chain,
        test_trending_projects,
        test_solana_projects,
        test_base_chain_projects,
        test_project_details,
        test_error_handling,
        test_limit_parameter,
    ]

    for test in tests:
        try:
            await test()
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "#"*60)
    print("# All tests completed!")
    print("#"*60)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
