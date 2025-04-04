import logging
import os
from functools import wraps

import dotenv
from flask import Flask, jsonify, request

from agents.base_agent import BaseAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()


def require_api_key(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        if not api_key or api_key != os.getenv("API_KEY"):
            return jsonify({"error": "Invalid or missing API key"}), 401
        return await f(*args, **kwargs)

    return decorated_function


class FlaskAgent:
    def __init__(self, core_agent=None):
        # Type check if core_agent is provided
        if core_agent is not None and not isinstance(core_agent, BaseAgent):
            raise TypeError(f"core_agent must be an instance of BaseAgent, got {type(core_agent).__name__}")

        if core_agent:
            super().__setattr__("_parent", core_agent)
        else:
            # Need to set _parent = self first before super().__init__()
            super().__setattr__("_parent", self)  # Bypass normal __setattr__
            super().__init__()

        # Initialize Flask specific stuff
        self._app = Flask(__name__)  # Store as _app to avoid delegation
        self._setup_routes()
        self.register_interface("api", self)

    def __getattr__(self, name):
        # Delegate to the parent instance for missing attributes/methods
        return getattr(self._parent, name)

    def __setattr__(self, name, value):
        if not hasattr(self, "_parent"):
            # During initialization, before _parent is set
            super().__setattr__(name, value)
        elif name == "_parent" or self is self._parent or name in self.__dict__:
            # Set local attributes (like _parent or already existing attributes)
            super().__setattr__(name, value)
        else:
            # Delegate attribute setting to the parent instance
            setattr(self._parent, name, value)

    def run(self, host="0.0.0.0", port=5005):
        """Run the Flask application"""
        if hasattr(self, "_app"):
            self._app.run(host=host, port=port, debug=False)
        else:
            raise RuntimeError("Flask app not initialized")

    def _setup_routes(self):
        # Example usage:
        # curl -X POST http://localhost:5000/message \
        #   -H "Content-Type: application/json" \
        #   -d '{"message": "Tell me about artificial intelligence"}'
        #
        # Response:
        # {
        #   "text": "AI is a field of computer science...",
        #   "image_url": "http://example.com/image.jpg"  # Optional
        # }
        @self._app.route("/message", methods=["POST"])
        @require_api_key
        async def handle_message():
            try:
                data = request.get_json()
                logger.info(data)
                if not data or "message" not in data:
                    return jsonify({"error": "No message provided"}), 400
                chat_id = None
                external_tools = data.get("tools", [])
                logger.info(external_tools)
                if "chat_id" in data:
                    chat_id = data["chat_id"]
                text_response, image_url, tool_calls = await self.handle_message(
                    data["message"], source_interface="api", chat_id=chat_id, external_tools=external_tools
                )
                print(tool_calls)
                if self._parent != self:
                    logger.info("Operating in shared mode with core agent")
                else:
                    logger.info("Operating in standalone mode")

                response = {}
                if image_url:
                    response["image_url"] = image_url
                if text_response:
                    response["text"] = text_response
                if tool_calls:
                    response["tool_calls"] = tool_calls
                return jsonify(response)
            except Exception as e:
                logger.error(f"Message handling failed: {str(e)}")
                return jsonify({"error": "Internal server error"}), 500


def main():
    agent = FlaskAgent()
    agent.run()


if __name__ == "__main__":
    try:
        logger.info("Starting Flask agent...")
        main()
    except KeyboardInterrupt:
        logger.info("\nFlask agent stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
