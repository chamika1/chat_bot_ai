# AI Chat Bot 🤖

A powerful Telegram AI Chat Bot built with Python, featuring advanced AI capabilities, web search, image analysis, and multiple personality modes.

## Features ✨

- 💬 Natural Language Processing with Groq AI
- 🔍 Web Search Integration
- 🖼️ Image Analysis and Generation
- 👥 Multiple Personality Modes
- 🌐 Web Search Integration
- 💾 Persistent Memory System
- 🔐 Channel-based Access Control

## Commands 📚

- `/start` - Start a fresh conversation
- `/help` - Show help menu
- `/clear` - Reset conversation history
- `/memory` - View chat statistics
- `/search [query]` - Search and analyze web results
- `/image [URL]` - Analyze an image in detail
- `/search_image [URL]` - Search info about an image
- `/generate [prompt]` - Create AI artwork
- `/role_girlfriend` - Switch to friendly chat mode
- `/role_assistant` - Switch to professional mode

## Tech Stack 🛠️

- Python 3.8+
- python-telegram-bot
- Groq AI API
- Flask
- DuckDuckGo Search API
- Gunicorn

## Setup and Installation 🚀

1. Clone the repository:
   ```bash
   git clone https://github.com/chamika1/chat_bot_ai.git
   cd chat_bot_ai
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - `TELEGRAM_TOKEN` - Your Telegram Bot Token
   - `GROQ_API_KEY` - Your Groq API Key

4. Run the bot:
   ```bash
   python main.py
   ```

## Deployment 🌐

This bot is configured for deployment on Render:

1. Fork this repository
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Add environment variables:
   - `TELEGRAM_TOKEN`
   - `GROQ_API_KEY`
5. Deploy!

## Project Structure 📁

```
chat_bot_ai/
├── main.py           # Main bot logic
├── wsgi.py          # Web server configuration
├── requirements.txt  # Python dependencies
├── render.yaml      # Render deployment config
├── start.sh         # Startup script
└── README.md        # Documentation
```

## Features in Detail 🔍

### AI Chat Capabilities
- Natural language understanding
- Context-aware conversations
- Multiple personality modes

### Image Processing
- Detailed image analysis
- Image-based web searches
- AI art generation

### Web Integration
- Real-time web searches
- Information synthesis
- Source citation

### Memory System
- Conversation persistence
- User preference storage
- Chat statistics

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Support 💬

Join our Telegram channel for updates and support: [Bot Land](https://t.me/+fUfz-TI9nGc1MWY1) 