import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.yahoo_finance_agent import YahooFinanceAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "aapl_price_history": {
        "input": {
            "query": "Get 1d OHLCV for AAPL for the last 6 months",
            "raw_data_only": False,
        },
        "description": "Natural language query for AAPL 1d OHLCV data for 6 months",
    },
    "btc_indicators": {
        "input": {
            "query": "Give me a 1h indicator snapshot for BTC-USD",
            "raw_data_only": False,
        },
        "description": "Natural language query for BTC-USD 1h indicator snapshot",
    },
    "tsla_technical_direct": {
        "input": {
            "tool": "indicator_snapshot",
            "tool_arguments": {"symbol": "TSLA", "interval": "1d", "period": "3mo"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for TSLA technical analysis with raw data",
    },
    "eth_price_history_direct": {
        "input": {
            "tool": "fetch_price_history",
            "tool_arguments": {"symbol": "ETH-USD", "interval": "1h", "period": "5d"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for ETH-USD price history with 1h interval",
    },
    "tsla_signal_analysis": {
        "input": {
            "query": "Signal summary for TSLA on 1d timeframe",
            "raw_data_only": False,
        },
        "description": "Natural language query for TSLA trading signal summary",
    },
    "googl_date_range": {
        "input": {
            "tool": "fetch_price_history",
            "tool_arguments": {
                "symbol": "GOOGL",
                "interval": "1d",
                "start_date": "2024-01-01",
                "end_date": "2024-06-30",
            },
            "raw_data_only": False,
        },
        "description": "Direct tool call for GOOGL with specific date range",
    },
    # Crypto test cases
    "sol_technical_analysis": {
        "input": {"query": "Show me technical analysis for SOL-USD"},
        "description": "Natural language query for SOL-USD technical analysis",
    },
    "doge_price_data": {
        "input": {"query": "Get recent price data for DOGE-USD"},
        "description": "Natural language query for DOGE-USD recent price data",
    },
    "ada_trading_signal": {
        "input": {"query": "What's the trading signal for ADA-USD?"},
        "description": "Natural language query for ADA-USD trading signal",
    },
    # Error handling test
    "invalid_interval": {
        "input": {
            "tool": "fetch_price_history",
            "tool_arguments": {"symbol": "AAPL", "interval": "5m"},  # Invalid interval
            "raw_data_only": True,
        },
        "description": "Error handling test with invalid interval (5m not supported)",
    },
    # Stock symbols tests
    "msft_indicators": {
        "input": {
            "tool": "indicator_snapshot",
            "tool_arguments": {"symbol": "MSFT", "interval": "1d"},
            "raw_data_only": False,
        },
        "description": "Direct tool call for MSFT indicator snapshot",
    },
    "amzn_indicators": {
        "input": {
            "tool": "indicator_snapshot",
            "tool_arguments": {"symbol": "AMZN", "interval": "1d"},
            "raw_data_only": False,
        },
        "description": "Direct tool call for AMZN indicator snapshot",
    },
    "nvda_indicators": {
        "input": {
            "tool": "indicator_snapshot",
            "tool_arguments": {"symbol": "NVDA", "interval": "1d"},
            "raw_data_only": False,
        },
        "description": "Direct tool call for NVDA indicator snapshot",
    },
    # Major crypto technical analysis
    "btc_technical": {
        "input": {
            "tool": "indicator_snapshot",
            "tool_arguments": {"symbol": "BTC-USD", "interval": "1d", "period": "1mo"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for BTC-USD technical indicators",
    },
    "eth_technical": {
        "input": {
            "tool": "indicator_snapshot",
            "tool_arguments": {"symbol": "ETH-USD", "interval": "1d", "period": "1mo"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for ETH-USD technical indicators",
    },
    "bnb_technical": {
        "input": {
            "tool": "indicator_snapshot",
            "tool_arguments": {"symbol": "BNB-USD", "interval": "1d", "period": "1mo"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for BNB-USD technical indicators",
    },
    "sol_technical": {
        "input": {
            "tool": "indicator_snapshot",
            "tool_arguments": {"symbol": "SOL-USD", "interval": "1d", "period": "1mo"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for SOL-USD technical indicators",
    },
    "xrp_technical": {
        "input": {
            "tool": "indicator_snapshot",
            "tool_arguments": {"symbol": "XRP-USD", "interval": "1d", "period": "1mo"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for XRP-USD technical indicators",
    },
    # Natural language test cases
    "apple_trend": {
        "input": {"query": "What's the current trend for Apple stock?"},
        "description": "Natural language query for Apple stock trend",
    },
    "bitcoin_monthly": {
        "input": {"query": "Show me Bitcoin price movements over the last month"},
        "description": "Natural language query for Bitcoin monthly price movements",
    },
    "ethereum_signals": {
        "input": {"query": "Give me trading signals for Ethereum"},
        "description": "Natural language query for Ethereum trading signals",
    },
    "tesla_performance": {
        "input": {"query": "How is Tesla performing technically?"},
        "description": "Natural language query for Tesla technical performance",
    },
    "microsoft_ohlcv": {
        "input": {"query": "Get me OHLCV data for Microsoft"},
        "description": "Natural language query for Microsoft OHLCV data",
    },
    # Symbol validation test cases
    "invalid_symbol_fakecoin": {
        "input": {
            "tool": "fetch_price_history",
            "tool_arguments": {"symbol": "FAKECOIN-USD", "interval": "1d"},
            "raw_data_only": True,
        },
        "description": "Test invalid symbol rejection (FAKECOIN-USD)",
    },
    "invalid_symbol_random": {
        "input": {
            "tool": "indicator_snapshot",
            "tool_arguments": {"symbol": "ABR", "interval": "1d"},
            "raw_data_only": True,
        },
        "description": "",
    },
    "invalid_symbol_memecoin": {
        "input": {
            "tool": "fetch_price_history",
            "tool_arguments": {"symbol": "NEWMEME-USD", "interval": "1h"},
            "raw_data_only": True,
        },
        "description": "Test invalid symbol rejection (NEWMEME-USD)",
    },
    "invalid_symbol_numeric": {
        "input": {
            "tool": "indicator_snapshot",
            "tool_arguments": {"symbol": "12345", "interval": "1d"},
            "raw_data_only": True,
        },
        "description": "Test invalid symbol rejection (12345)",
    },
    # Valid symbols that should work
    "valid_symbol_spy": {
        "input": {
            "tool": "fetch_price_history",
            "tool_arguments": {"symbol": "SPY", "interval": "1d", "period": "5d"},
            "raw_data_only": True,
        },
        "description": "Test valid ETF symbol (SPY)",
    },
    "valid_symbol_qqq": {
        "input": {
            "tool": "indicator_snapshot",
            "tool_arguments": {"symbol": "QQQ", "interval": "1d"},
            "raw_data_only": True,
        },
        "description": "Test valid ETF symbol (QQQ)",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(YahooFinanceAgent, TEST_CASES))
