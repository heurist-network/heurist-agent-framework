# You.com Search Integration

This integration adds You.com as a search provider to the Heurist Agent Framework's SearchClient system.

## Features

- **Unified Interface**: Integrates seamlessly with the existing SearchClient abstraction
- **Dual Authentication**: Supports both authenticated (API key) and keyless modes
- **Rate Limiting**: Built-in rate limiting support
- **Error Handling**: Graceful error handling with structured responses
- **Multi-Result Types**: Handles both web and news search results from You.com API

## Usage

### Basic Usage (Keyless)

```python
from core.clients.search_client import SearchClient

# Create You.com search client (keyless mode - 100 free searches/day)
search_client = SearchClient('youcom')

# Perform search
results = await search_client.search('AI agent frameworks')
print(f"Found {len(results['data'])} results")
```

### Authenticated Usage

```python
import os
from core.clients.search_client import SearchClient

# Create You.com search client with API key
api_key = os.getenv('YDC_API_KEY')
search_client = SearchClient('youcom', api_key=api_key)

# Perform search with higher rate limits
results = await search_client.search('latest AI research')
```

### Custom Configuration

```python
# Custom API URL and rate limiting
search_client = SearchClient(
    'youcom', 
    api_key='your_key_here',
    api_url='https://custom.youcom.api',
    rate_limit=2  # 2 seconds between requests
)
```

## Environment Variables

- `YDC_API_KEY`: Your You.com API key (optional for keyless access)
- `YOUCOM_BASE_URL`: Custom base URL (default: https://api.you.com)

## Response Format

The You.com client returns results in the standard SearchClient format:

```python
{
    "data": [
        {
            "url": "https://example.com",
            "title": "Page Title",
            "markdown": "Page content snippet...",
            "type": "web"  # or "news"
        },
        # ... more results
    ]
}
```

## Rate Limits

- **Keyless Mode**: 100 searches per day
- **Authenticated Mode**: Varies by API plan
- **Built-in Rate Limiting**: Configurable delay between requests

## Error Handling

The integration handles errors gracefully:
- Network timeouts return empty results
- Authentication errors are logged and return empty results
- Invalid responses are handled safely

## Testing

Run the demo script to test the integration:

```bash
# Without API key (keyless mode)
python examples/youcom_search_demo.py

# With API key
YDC_API_KEY=your_key_here python examples/youcom_search_demo.py
```

## Implementation Details

- **File**: `core/clients/search/youcom_client.py`
- **Base Class**: Extends `BaseSearchClient`
- **HTTP Client**: Uses `requests` (already a project dependency)
- **API Endpoint**: `/v1/agents/search`
- **Threading**: Async-safe using `asyncio.get_event_loop().run_in_executor()`