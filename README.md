<div align="center">
    <img src="./docs/img/agent-framework-poster.jpg" alt="Heurist Agent Framework Banner" width="100%" />
</div>

# Heurist Agent Framework
*The Raspberry Pi of Agent Frameworks*

A flexible multi-interface AI agent framework that can interact through various platforms including Telegram, Discord, Twitter, Farcaster, and REST API.

Grab a Heurist API Key instantly for free by using the code 'agent' while submitting the form at https://heurist.ai/dev-access
## Overview

The Heurist Agent Framework is built on a modular architecture that allows an AI agent to:
- Process text messages and generate responses
- Generate and handle images
- Process voice messages (transcription and text-to-speech)
- Interact across multiple platforms with consistent behavior

## Features

- 🤖 Core Agent functionality with LLM integration
- 🖼️ Image generation capabilities
- 🎤 Voice processing (transcription and TTS)
- 🔌 Multiple interface support:
  - Telegram bot
  - Discord bot
  - Twitter automation
  - Farcaster integration
  - REST API

<div align="center">
<img src="./docs/img/HFA_2.png" alt="Heurist Agent Framework" width="500">
</div>

## Installation

1. Clone the repository:

```bash
git clone https://github.com/heurist-network/heurist-agent-framework.git
cd heurist-agent-framework
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
see `.env.example`


## Usage

### Running Different Interfaces

1. Telegram Agent:
```bash
python main_telegram.py
```

2. Discord Agent:
```bash
python main_discord.py
```

3. REST API:
```bash
python main_api.py
```

4. Twitter Bot (Posting):
```bash
python main_twitter.py
```

### API Endpoints

The REST API provides the following endpoints:

- POST `/message`
  - Request body: `{"message": "Your message here"}`
  - Response: `{"text": "Response text", "image_url": "Optional image URL"}`

Example:
```bash
curl -X POST http://localhost:5005/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about artificial intelligence"}'
```

## Architecture

The framework follows a modular design:

1. Core Agent (`core_agent.py`)
   - Handles core functionality
   - Manages LLM interactions
   - Processes images and voice

2. Interfaces
   - Telegram (`interfaces/telegram_agent.py`)
   - Discord (`interfaces/discord_agent.py`)
   - API (`interfaces/flask_agent.py`)
   - Twitter (`interfaces/twitter_agent.py`)
   - Farcaster (`interfaces/farcaster_agent.py`)

Each interface inherits from the CoreAgent and implements platform-specific handling.

<div align="center">
<img src="./docs/img/HFA_1.png" alt="Heurist Agent Framework" width="500">
</div>


## Configuration

The framework uses YAML configuration for prompts and agent behavior. Configure these in:
```
config/prompts.yaml
```

## Development

To add a new interface:

1. Create a new class inheriting from `CoreAgent`
2. Implement platform-specific handlers
3. Use core agent methods for processing:
   - `handle_message()`
   - `handle_image_generation()`
   - `transcribe_audio()`

## License

MIT License - See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. Join the Heurist Ecosystem Builder telegram https://t.me/heuristsupport

## WIP

More features and refinement are on the way!

Example structure for finalized tweet flow on the works:

<div align="center">
<img src="./docs/img/TwitterFinalFLow.png" alt="Heurist Agent Framework" width="500">
</div>

*"_eval" param indicates requires agent to evaluate if it should respond*

*"_HITL" param indicates requirment to activate Human In The Loop flow*
