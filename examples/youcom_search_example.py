#!/usr/bin/env python3
"""
Example demonstrating You.com search integration with Heurist Agent Framework.

This example shows how to use the new YouComClient for web search queries.
Supports both authenticated (with YDC_API_KEY) and keyless operation.
"""

import asyncio
import os
from core.clients.search_client import SearchClient


async def main():
    """Demonstrate You.com search integration."""
    
    # Create a You.com search client
    # API key is optional - will use YDC_API_KEY env var if available
    # Falls back to keyless operation (100 free searches/day) without key
    search_client = SearchClient(client_type="youcom")
    
    # Example search query
    query = "AI agent frameworks 2026"
    print(f"Searching for: {query}")
    print("-" * 50)
    
    try:
        # Perform the search
        results = await search_client.search(query)
        
        # Display results
        if results["data"]:
            print(f"Found {len(results['data'])} results:")
            print()
            
            for i, result in enumerate(results["data"], 1):
                print(f"{i}. {result.get('title', 'No title')}")
                print(f"   URL: {result.get('url', 'No URL')}")
                print(f"   Type: {result.get('type', 'web')}")
                print(f"   Description: {result.get('markdown', 'No description')[:150]}...")
                print()
        else:
            print("No results found.")
            
    except Exception as e:
        print(f"Search error: {e}")
        print()
        print("Troubleshooting:")
        print("1. For authenticated usage, set YDC_API_KEY environment variable")
        print("2. For keyless usage, ensure you're within daily quota (100 searches/day)")
        print("3. Check network connectivity to api.you.com")


if __name__ == "__main__":
    # Check if we have API key configured
    api_key_configured = bool(os.getenv("YDC_API_KEY") or os.getenv("YOUCOM_API_KEY"))
    
    print("Heurist Agent Framework - You.com Search Integration Example")
    print("=" * 60)
    
    if api_key_configured:
        print("✓ API key detected - using authenticated access")
    else:
        print("ℹ No API key - using keyless access (100 free searches/day)")
    
    print()
    
    # Run the example
    asyncio.run(main())