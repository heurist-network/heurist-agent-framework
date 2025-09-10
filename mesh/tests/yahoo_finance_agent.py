import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.yahoo_finance_agent import YahooFinanceAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = YahooFinanceAgent()
    try:
        # Test 1: Natural language query for stock price history
        agent_input_stock_history = {
            "query": "Get 1d OHLCV for AAPL for the last 6 months",
            "raw_data_only": False,
        }
        agent_output_stock_history = await agent.handle_message(agent_input_stock_history)

        # Test 2: Natural language query for crypto indicator snapshot
        agent_input_crypto_indicators = {
            "query": "Give me a 1h indicator snapshot for BTC-USD",
            "raw_data_only": False,
        }
        agent_output_crypto_indicators = await agent.handle_message(agent_input_crypto_indicators)

        # Test 3: Direct tool call for stock technical analysis
        agent_input_stock_technical = {
            "tool": "indicator_snapshot",
            "tool_arguments": {"symbol": "TSLA", "interval": "1d", "period": "3mo"},
            "raw_data_only": True,
        }
        agent_output_stock_technical = await agent.handle_message(agent_input_stock_technical)

        # Test 4: Direct tool call for crypto price history
        agent_input_crypto_history = {
            "tool": "fetch_price_history",
            "tool_arguments": {"symbol": "ETH-USD", "interval": "1h", "period": "5d"},
            "raw_data_only": True,
        }
        agent_output_crypto_history = await agent.handle_message(agent_input_crypto_history)

        # Test 5: Natural language query for technical analysis
        agent_input_analysis = {
            "query": "Signal summary for TSLA on 1d timeframe",
            "raw_data_only": False,
        }
        agent_output_analysis = await agent.handle_message(agent_input_analysis)

        # Test 6: Test with date range
        agent_input_date_range = {
            "tool": "fetch_price_history",
            "tool_arguments": {
                "symbol": "GOOGL",
                "interval": "1d",
                "start_date": "2024-01-01",
                "end_date": "2024-06-30",
            },
            "raw_data_only": False,
        }
        agent_output_date_range = await agent.handle_message(agent_input_date_range)

        # Test 7: Test multiple crypto symbols
        crypto_test_cases = [
            {"query": "Show me technical analysis for SOL-USD"},
            {"query": "Get recent price data for DOGE-USD"},
            {"query": "What's the trading signal for ADA-USD?"},
        ]

        crypto_results = {}
        for i, test_case in enumerate(crypto_test_cases):
            result = await agent.handle_message(test_case)
            crypto_results[f"crypto_case_{i + 1}"] = {"input": test_case, "output": result}

        # Test 8: Test error handling with invalid interval
        agent_input_invalid = {
            "tool": "fetch_price_history",
            "tool_arguments": {"symbol": "AAPL", "interval": "5m"},  # Invalid interval
            "raw_data_only": True,
        }
        agent_output_invalid = await agent.handle_message(agent_input_invalid)

        # Test 9: Test with various stock symbols
        stock_symbols = ["MSFT", "AMZN", "NVDA"]
        stock_results = {}
        for symbol in stock_symbols:
            test_input = {
                "tool": "indicator_snapshot",
                "tool_arguments": {"symbol": symbol, "interval": "1d"},
                "raw_data_only": False,
            }
            result = await agent.handle_message(test_input)
            stock_results[f"stock_{symbol}"] = {"input": test_input, "output": result}

        # Test 10: Test with major crypto tokens from the TOP_30 list
        major_cryptos = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD"]
        crypto_technical_results = {}
        for crypto in major_cryptos:
            test_input = {
                "tool": "indicator_snapshot",
                "tool_arguments": {"symbol": crypto, "interval": "1d", "period": "1mo"},
                "raw_data_only": True,
            }
            result = await agent.handle_message(test_input)
            crypto_technical_results[f"crypto_{crypto.replace('-USD', '')}"] = {"input": test_input, "output": result}

        # Test 11: Natural language queries for various scenarios
        natural_language_tests = [
            {"query": "What's the current trend for Apple stock?"},
            {"query": "Show me Bitcoin price movements over the last month"},
            {"query": "Give me trading signals for Ethereum"},
            {"query": "How is Tesla performing technically?"},
            {"query": "Get me OHLCV data for Microsoft"},
        ]

        nl_results = {}
        for i, test_case in enumerate(natural_language_tests):
            result = await agent.handle_message(test_case)
            nl_results[f"nl_case_{i + 1}"] = {"input": test_case, "output": result}

        # Save the test inputs and outputs to a YAML file for further inspection
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "stock_price_history": {"input": agent_input_stock_history, "output": agent_output_stock_history},
            "crypto_indicators": {"input": agent_input_crypto_indicators, "output": agent_output_crypto_indicators},
            "stock_technical_analysis": {"input": agent_input_stock_technical, "output": agent_output_stock_technical},
            "crypto_price_history": {"input": agent_input_crypto_history, "output": agent_output_crypto_history},
            "trading_signal_analysis": {"input": agent_input_analysis, "output": agent_output_analysis},
            "date_range_test": {"input": agent_input_date_range, "output": agent_output_date_range},
            "crypto_test_cases": crypto_results,
            "invalid_interval_test": {"input": agent_input_invalid, "output": agent_output_invalid},
            "stock_symbols_test": stock_results,
            "major_cryptos_technical": crypto_technical_results,
            "natural_language_tests": nl_results,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
