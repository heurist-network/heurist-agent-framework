# You.com Search Integration

This document describes the You.com search integration added to the Heurist Agent Framework.

## Overview

The You.com integration provides web search capabilities through You.com's Search API, supporting both authenticated and keyless operation modes. It seamlessly integrates with the framework's existing search client architecture.

## Features

- **Dual Operation Modes**: Works with or without API keys
- **Keyless Access**: 100 free searches per day per IP without authentication
- **Authenticated Access**: Higher quotas and enhanced features with API key
- **Multiple Result Types**: Supports both web and news search results
- **Rate Limiting**: Built-in request throttling to respect API limits
- **Error Handling**: Graceful degradation on API errors or network issues

## Configuration

### Environment Variables

You.com search can be configured using environment variables:

```bash
# Primary API key variable (recommended)
YDC_API_KEY=your_you_com_api_key

# Alternative API key variable (for compatibility)
YOUCOM_API_KEY=your_you_com_api_key
```

### Usage in Code

```python
from core.clients.search_client import SearchClient

# Using environment variable for API key
search_client = SearchClient(client_type="youcom")

# Or explicitly providing API key
search_client = SearchClient(client_type="youcom", api_key="your_api_key")

# Keyless operation (no API key required)
keyless_client = SearchClient(client_type="youcom", api_key="")
```

## API Endpoints

The integration uses You.com's Agent Search API:

- **Base URL**: `https://api.you.com`
- **Search Endpoint**: `/v1/agents/search`
- **Method**: GET
- **Rate Limits**: Varies by plan (keyless: 100/day, authenticated: based on plan)

## Response Format

The client normalizes You.com responses to match the framework's standard format:

```python
{
    "data": [
        {
            "url": "https://example.com",
            "title": "Page Title",
            "markdown": "Page description or content",
            "type": "web"  # or "news"
        }
    ]
}
```

## Error Handling

The client handles various error conditions gracefully:

- **401 Unauthorized**: Invalid or missing API key
- **429 Rate Limited**: Too many requests, suggests waiting
- **Network Errors**: Connection issues, timeouts
- **API Errors**: Malformed responses, service unavailable

All errors result in an empty result set (`{"data": []}`) and log appropriate error messages.

## Examples

### Basic Search

```python
import asyncio
from core.clients.search_client import SearchClient

async def search_example():
    client = SearchClient(client_type="youcom")
    results = await client.search("AI agent frameworks")
    
    for result in results["data"]:
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Type: {result['type']}")
        print()

asyncio.run(search_example())
```

### With Custom Rate Limiting

```python
# Slower rate limiting for keyless usage
client = SearchClient(
    client_type="youcom", 
    rate_limit=2  # 2 seconds between requests
)
```

### Integration in Agents

You.com search can be easily integrated into existing agents:

```python
class ResearchAgent:
    def __init__(self):
        self.search_client = SearchClient(client_type="youcom")
    
    async def research_topic(self, topic: str):
        results = await self.search_client.search(f"latest research {topic}")
        return self.analyze_results(results["data"])
```

## Testing

Run the test suite to verify the integration:

```bash
# From the project root
python -m pytest core/clients/search/test_youcom_client.py -v
```

## Troubleshooting

### Common Issues

1. **"Authentication failed"**: Set `YDC_API_KEY` environment variable
2. **"Rate limit exceeded"**: Wait before making more requests or upgrade API plan
3. **Empty results**: Check network connectivity and API quotas

### Debugging

Enable debug logging to see detailed API interactions:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### API Key Sources (Priority Order)

1. Explicit `api_key` parameter in constructor
2. `YDC_API_KEY` environment variable
3. `YOUCOM_API_KEY` environment variable
4. Keyless operation (empty string)

## Performance Considerations

- **Keyless Limits**: 100 searches/day per IP
- **Rate Limiting**: Default 1 second between requests
- **Timeout**: 15 second default request timeout
- **Caching**: No built-in caching (implement at application level if needed)

## Security Notes

- API keys are never logged or exposed in error messages
- All requests use HTTPS
- Rate limiting prevents accidental quota exhaustion
- Keyless operation provides safe evaluation without credentials

## Migration from Other Providers

Switching from other search providers is straightforward:

```python
# From Exa
old_client = SearchClient(client_type="exa", api_key="exa_key")

# To You.com
new_client = SearchClient(client_type="youcom", api_key="ydc_key")

# Same interface, different provider
results = await new_client.search("same query")
```

## Support

For issues specific to the You.com API:
- You.com API Documentation: https://docs.you.com
- You.com Developer Support: https://you.com/support

For integration issues within Heurist Agent Framework:
- GitHub Issues: https://github.com/heurist-network/heurist-agent-framework/issues