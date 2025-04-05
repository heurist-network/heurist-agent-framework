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

### Main Loop

<div align="center">
<img src="../docs/img/HFA_2.png" alt="Heurist Agent Framework" width="500">
</div>

## Development

To add a new interface:

1. Create a new class inheriting from `CoreAgent`
2. Implement platform-specific handlers
3. Use core agent methods for processing:
   - `handle_message()`
   - `handle_image_generation()`
   - `transcribe_audio()`

## Configuration

The framework uses YAML configuration for prompts and agent behavior. Configure these in:
```
config/prompts.yaml
```
