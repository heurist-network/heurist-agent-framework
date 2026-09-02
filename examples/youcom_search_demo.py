#!/usr/bin/env python3
"""
You.com Search Client Demo

This example demonstrates how to use You.com search within the Heurist Agent Framework.
It shows both authenticated (with API key) and keyless usage modes.

Requirements:
- Set YDC_API_KEY environment variable for authenticated access (optional)
- Install dependencies: uv sync
- Run: python examples/youcom_search_demo.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.clients.search_client import SearchClient


async def main():
    """Demonstrate You.com search integration."""
    
    print("=== You.com Search Client Demo ===\n")
    
    # Get API key from environment (optional for keyless access)
    api_key = os.getenv("YDC_API_KEY", "")
    
    if api_key:
        print(f"✓ Using authenticated mode with API key: {api_key[:8]}...")
    else:
        print("ℹ  Using keyless mode (100 free searches/day)")
    
    print()
    
    try:
        # Create You.com search client
        search_client = SearchClient("youcom", api_key=api_key)
        print("✓ You.com search client initialized")
        
        # Test search queries
        test_queries = [
            "AI agent frameworks 2026",
            "latest developments in MCP protocol",
            "heurist network blockchain agents"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n--- Test Query {i}: {query} ---")
            
            try:
                # Perform the search
                results = await search_client.search(query, timeout=10000)
                
                if results["data"]:
                    print(f"✓ Found {len(results['data'])} results")
                    
                    # Display first few results
                    for j, result in enumerate(results["data"][:3], 1):
                        print(f"  {j}. {result['title']}")
                        print(f"     URL: {result['url']}")
                        print(f"     Type: {result.get('type', 'web')}")
                        if result['markdown']:
                            snippet = result['markdown'][:100] + "..." if len(result['markdown']) > 100 else result['markdown']
                            print(f"     Snippet: {snippet}")
                        print()
                else:
                    print("⚠  No results found")
                
            except Exception as e:
                print(f"✗ Search failed: {e}")
        
        print("\n=== Integration Test Complete ===")
        print("You.com search client is working correctly!")
        
    except Exception as e:
        print(f"✗ Failed to initialize search client: {e}")
        print("Please check your configuration and try again.")


if __name__ == "__main__":
    # Run the async demo
    asyncio.run(main())