#!/usr/bin/env python3
"""
Test script for ProjectKnowledgeAgent.
Tests semantic_search and get_project with test cases: "stable" and "rocket"
"""

import asyncio
import json
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from mesh.agents.project_knowledge_agent import ProjectKnowledgeAgent

TEST_CASES = [
    {"name": "stable", "url": "https://www.stable.xyz/"},
    {"name": "rocket", "url": "https://www.rootdata.com/Projects/detail/Rocket?k=MjI1MzI%3D"},
]


def print_section(title: str):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


async def test_semantic_search_by_name(agent: ProjectKnowledgeAgent, name: str):
    """Test semantic_search tool with name parameter (lexical search mode)."""
    print_section(f"Testing semantic_search with name='{name}' (lexical mode)")
    
    result = await agent._handle_tool_logic(
        "semantic_search",
        {"name": name, "limit": 10},
        session_context={}
    )
    
    if "error" in result:
        print(f"   ✗ Error: {result['error']}")
        print(f"   Note: This requires lexical_search_projects function in database")
        return
    
    results = result.get("results", [])
    print(f"   ✓ Found {len(results)} results")
    
    if results:
        best_match = results[0]
        print(f"\n   Best Match:")
        print(f"   - Name: {best_match.get('name')}")
        print(f"   - Token Symbol: {best_match.get('token_symbol')}")
        print(f"   - One-liner: {best_match.get('one_liner', 'NULL')}")
        print(f"   - Description: {best_match.get('description', 'NULL')}")
        print(f"   - Twitter URL: {best_match.get('twitter_url', 'NULL')}")
        print(f"   - CoinGecko Slug: {best_match.get('coingecko_slug', 'NULL')}")
        print(f"   - Is Best Match: {best_match.get('is_best_match')}")
        print(f"   - Latest Event Date: {best_match.get('latest_event_date')}")
        print(f"   - Updated At: {best_match.get('updated_at')}")
        print(f"   - Similarity Score: {best_match.get('similarity_score')}")


async def test_semantic_search_natural_language(agent: ProjectKnowledgeAgent, query: str):
    """Test semantic_search tool with natural language query."""
    print_section(f"Testing semantic_search with query='{query}' (semantic mode)")
    
    result = await agent._handle_tool_logic(
        "semantic_search",
        {"query": query, "limit": 5},
        session_context={}
    )
    
    if "error" in result:
        print(f"   ✗ Error: {result['error']}")
        return
    
    results = result.get("results", [])
    print(f"   ✓ Found {len(results)} results")
    
    if results:
        best_match = results[0]
        print(f"\n   Best Match:")
        print(f"   - Name: {best_match.get('name')}")
        print(f"   - Token Symbol: {best_match.get('token_symbol')}")
        print(f"   - One-liner: {best_match.get('one_liner', 'NULL')}")
        print(f"   - Description: {best_match.get('description', 'NULL')}")
        print(f"   - Twitter URL: {best_match.get('twitter_url', 'NULL')}")
        print(f"   - CoinGecko Slug: {best_match.get('coingecko_slug', 'NULL')}")
        print(f"   - Is Best Match: {best_match.get('is_best_match')}")
        print(f"   - Latest Event Date: {best_match.get('latest_event_date')}")
        print(f"   - Updated At: {best_match.get('updated_at')}")
        print(f"   - Similarity Score: {best_match.get('similarity_score')}")
        
        # Verify best match has details
        has_details = (
            best_match.get('twitter_url') is not None or
            best_match.get('coingecko_slug') is not None or
            best_match.get('one_liner') is not None
        )
        if has_details:
            print(f"\n   ✓ Best match has details (twitter_url, coingecko_slug, or one_liner)")
        else:
            print(f"\n   ✗ Best match missing details")
        
        if len(results) > 1:
            print(f"\n   Other Matches (should only have name and description):")
            for i, match in enumerate(results[1:4], 1):
                print(f"\n   Match {i}:")
                print(f"   - Name: {match.get('name')}")
                print(f"   - Token Symbol: {match.get('token_symbol')}")
                print(f"   - Description: {match.get('description', 'NULL')}")
                print(f"   - One-liner: {match.get('one_liner', 'NULL')}")
                print(f"   - Twitter URL: {match.get('twitter_url', 'NULL')}")
                print(f"   - CoinGecko Slug: {match.get('coingecko_slug', 'NULL')}")
                print(f"   - Is Best Match: {match.get('is_best_match')}")
                
                # Verify other matches don't have details
                has_no_details = (
                    match.get('twitter_url') is None and
                    match.get('coingecko_slug') is None and
                    match.get('one_liner') is None
                )
                has_description = match.get('description') is not None
                
                if has_no_details and has_description:
                    print(f"   ✓ Match {i} correctly has only name and description")
                else:
                    print(f"   ✗ Match {i} has unexpected fields")


async def test_get_project(agent: ProjectKnowledgeAgent, name: str):
    """Test get_project tool."""
    print_section(f"Testing get_project with canonical_name='{name}'")
    
    result = await agent._handle_tool_logic(
        "get_project",
        {"canonical_name": name},
        session_context={}
    )
    
    if "error" in result:
        print(f"   ✗ Error: {result['error']}")
        return
    
    project = result.get("project")
    if project:
        print(f"   ✓ Found: {project.get('name')}")
        print(f"   - Token Symbol: {project.get('token_symbol')}")
        print(f"   - One-liner: {project.get('one_liner', 'NULL')}")
        print(f"   - Description: {project.get('description', 'NULL')[:100] if project.get('description') else 'NULL'}...")
        print(f"   - Twitter URL: {project.get('twitter_url', 'NULL')}")
        print(f"   - CoinGecko Slug: {project.get('coingecko_slug', 'NULL')}")
        print(f"   - Events: {len(project.get('events', []))} events")
        print(f"   - Team: {len(project.get('team', []))} members")
        print(f"   - Investors: {len(project.get('investors', []))} investors")
        print(f"   - Fundraising: {len(project.get('fundraising', []))} rounds")
        print(f"   - Exchanges: {len(project.get('exchanges', []))} exchanges")


async def main():
    print("=" * 60)
    print("  ProjectKnowledgeAgent Test Suite")
    print("  Test Cases: stable, rocket")
    print("=" * 60)
    
    agent = ProjectKnowledgeAgent()
    
    try:
        for test_case in TEST_CASES:
            name = test_case["name"]
            url = test_case["url"]
            
            print(f"\n\n{'#' * 60}")
            print(f"# Testing: {name}")
            print(f"# URL: {url}")
            print(f"{'#' * 60}")
            
            await test_semantic_search_by_name(agent, name)
            await test_semantic_search_natural_language(agent, f"projects related to {name}")
            await test_get_project(agent, name)
        
    finally:
        await agent.cleanup()
    
    print("\n\n" + "=" * 60)
    print("  Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

