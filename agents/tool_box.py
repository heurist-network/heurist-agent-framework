from typing import List, Dict, Any, Optional, Callable
import logging
from .tool_decorator import get_tool_schemas, tool
import aiohttp

logger = logging.getLogger(__name__)
## YOUR TOOLS GO HERE

class ToolBox:
    """Base class containing tool configurations and handlers"""
    
    def __init__(self):
        # Base tools configuration
        # Can be used to add tools by defining a function schema explicitly if needed
        self.tools_config = [
            # {
            #     "type": "function",
            #     "function": {
            #         "name": "generate_image",
            #         "description": "Generate an image based on a text prompt, any request to create an image should be handled by this tool, only use this tool if the user asks to create an image",
            #         "parameters": {
            #             "type": "object",
            #             "properties": {
            #                 "prompt": {"type": "string", "description": "The prompt to generate the image from"}
            #             },
            #             "required": ["prompt"]
            #         }
            #     }
            # },
        ]
        
        # Base handlers
        # Can be used to add handlers for schemas that were defined explicitly
        self.tool_handlers = {
            #"generate_image": self.handle_image_generation
        }

        self.decorated_tools = [
            self.get_crypto_price, 
            self.handle_image_generation,
            self.generate_image_prompt_for_posts,
            self.get_current_time
        ]

    @staticmethod
    @tool("Generate an image based on a text prompt")
    #async def handle_image_generation(self, args: Dict[str, Any], agent_context: Any) -> Dict[str, Any]: #example for explicitly defined schema
    async def handle_image_generation(prompt: str, agent_context: Any) -> Dict[str, Any]:
        """Generate an image based on a text prompt. Use this tool only when the user explicitly requests to create an image."""
        logger.info(prompt)
        try:
            image_url = await agent_context.handle_image_generation(prompt) #args['prompt'] for explicitly defined schema
            return {"image_url": image_url, "result": image_url}
        except Exception as e:
            logger.error(f"Image generation failed: {str(e)}")
            return {"error": str(e)}

    
    @staticmethod
    @tool("Get the current or historical price of a cryptocurrency in USD")
    async def get_crypto_price(ticker: str, timestamp: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the current or historical price of a cryptocurrency in USD from Binance.
        
        Args:
            ticker: The cryptocurrency ticker symbol (e.g., BTC, ETH, SOL)
            timestamp: Optional ISO format timestamp (e.g., '2024-03-20 14:30:00'). If not provided, returns current price
            
        Returns:
            Dict containing the price information
        """
        try:
            normalized_ticker = f"{ticker.upper()}USDT"
            
            if timestamp is None:
                # Get current price (existing logic)
                async with aiohttp.ClientSession() as session:
                    url = f"https://api.binance.com/api/v3/ticker/price?symbol={normalized_ticker}"
                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.json()
                            price = float(data['price'])
                            logger.info(f"The current price for {normalized_ticker}: ${price:.2f}")
                            return {"result": f"The current price for {normalized_ticker}: ${price:.2f}"}
            else:
                # Get historical price
                from datetime import datetime
                import time
                
                # Convert timestamp to milliseconds
                dt = datetime.fromisoformat(timestamp)
                timestamp_ms = int(dt.timestamp() * 1000)
                
                async with aiohttp.ClientSession() as session:
                    # Get klines (candlestick) data around the specified time
                    url = f"https://api.binance.com/api/v3/klines"
                    params = {
                        "symbol": normalized_ticker,
                        "interval": "1m",  # 1 minute interval
                        "startTime": timestamp_ms - 60000,  # 1 minute before
                        "endTime": timestamp_ms + 60000,    # 1 minute after
                        "limit": 1
                    }
                    
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            if data:
                                price = float(data[0][4])  # Close price
                                logger.info(f"The price for {normalized_ticker} at {timestamp}: ${price:.2f}")
                                return {"result": f"The price for {normalized_ticker} at {timestamp}: ${price:.2f}"}
                            return {"error": f"No price data available for {normalized_ticker} at {timestamp}"}
            
            error_msg = f"Failed to get price for {normalized_ticker}"
            logger.error(error_msg)
            return {"error": error_msg}
                        
        except ValueError as ve:
            error_msg = f"Invalid timestamp format. Please use ISO format (e.g., '2024-03-20 14:30:00'): {str(ve)}"
            logger.error(error_msg)
            return {"error": error_msg}
        except Exception as e:
            error_msg = f"Error getting crypto price: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}

    @staticmethod
    @tool("Generate an image prompt based on text input")
    async def generate_image_prompt_for_posts(text: str, agent_context: Any) -> Dict[str, str]:
        """
        Generate a detailed image prompt using the core agent's image prompt generator.
        Use this tool when you need to create an optimized prompt for image generation.
        IMPORTANT: This tool is only for image generation for posts, and images about you.
        IF the request is simple, just use image generation tool instead.
        
        Args:
            text: The input text to base the image prompt on
            agent_context: The core agent context
            
        Returns:
            Dict containing the generated image prompt
        """
        try:
            prompt = await agent_context.generate_image_prompt(text)
            return {"result": prompt} if prompt else {"error": "Failed to generate prompt"}
        except Exception as e:
            logger.error(f"Image prompt generation failed: {str(e)}")
            return {"error": str(e)}

    @staticmethod
    @tool("Get the current time in ISO format")
    async def get_current_time() -> Dict[str, str]:
        """
        Get the current time in ISO format.
        
        Returns:
            Dict containing the current time in ISO format
        """
        from datetime import datetime
        try:
            current_time = datetime.now().isoformat(timespec='seconds')
            return {"result": current_time}
        except Exception as e:
            logger.error(f"Error getting current time: {str(e)}")
            return {"error": str(e)}