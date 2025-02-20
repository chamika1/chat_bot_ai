# AI Chat Bot with Multiple Personalities 🤖

A versatile and powerful Telegram chatbot that combines advanced AI capabilities with multiple personality modes. Switch between a professional assistant for work and learning, or a friendly companion for casual chats. Features include web search integration, image analysis, AI art generation, and persistent memory management.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-✓-blue)](https://core.telegram.org/bots/api)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Groq AI](https://img.shields.io/badge/Groq%20AI-Powered-orange)](https://groq.com)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 🌟 Features

- 💬 Natural conversation with AI
- 🔄 Multiple personality modes (Assistant & Girlfriend)
- 🔍 Web search integration with DuckDuckGo
- 🖼️ Image analysis and search capabilities
- 🎨 AI artwork generation
- 💾 Persistent conversation memory
- 🔒 Privacy-focused design
- ⚡ Fast response times with Groq AI

## 🚀 Deployment Options

### Local Deployment

1. **Clone the repository**
```bash
git clone https://github.com/chamika1/ai_chat_bot.git
cd ai_chat_bot
```

2. **Set up a virtual environment**
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file in the project root:
```env
TELEGRAM_TOKEN=your_telegram_token_here
GROQ_API_KEY=your_groq_api_key_here
```

5. **Run the bot**
```bash
python main.py
```

### Deploy to Render

1. **Fork this repository** to your GitHub account

2. **Create a Render account** at https://render.com if you haven't already

3. **Create a new Web Service**
   - Click "New +" in your Render dashboard
   - Select "Web Service"
   - Connect your GitHub repository
   - Choose the repository you forked

4. **Configure the service**
   - Name: `ai-chat-bot` (or your preferred name)
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
   - Select the branch to deploy

5. **Add environment variables**
   In the Render dashboard, add these environment variables:
   - `TELEGRAM_TOKEN`: Your Telegram bot token
   - `GROQ_API_KEY`: Your Groq API key

6. **Deploy**
   - Click "Create Web Service"
   - Wait for the deployment to complete

7. **Verify deployment**
   - Check the logs in Render dashboard
   - Test your bot on Telegram

### Important Deployment Notes

1. **Environment Variables**
   - Keep your tokens secure
   - Never commit `.env` file
   - Use Render's environment variables section

2. **Persistence**
   - Bot memory is stored in-memory
   - For persistence, consider adding a database

3. **Scaling**
   - Free tier has limitations
   - Upgrade for better performance
   - Monitor usage in Render dashboard

4. **Troubleshooting**
   - Check Render logs for errors
   - Verify environment variables
   - Ensure all dependencies are listed in requirements.txt

## 📋 Prerequisites

Before running the bot, make sure you have:

- Python 3.8 or higher installed
- A Telegram Bot Token (get it from [@BotFather](https://t.me/botfather))
- A Groq API Key (obtain from [Groq's website](https://groq.com))
- Internet connection

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/chamika1/ai_chat_bot.git
cd ai_chat_bot
```

2. **Set up a virtual environment**
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file in the project root:
```env
TELEGRAM_TOKEN=your_telegram_token_here
GROQ_API_KEY=your_groq_api_key_here
```

5. **Run the bot**
```bash
python main.py
```

## 💡 Usage Guide

### Basic Commands
- `/start` - Begin chatting with the bot
- `/help` - View all available commands
- `/clear` - Reset conversation history
- `/memory` - View chat statistics

### Personality Modes
- `/role_assistant` - Switch to professional assistant mode
  - Focused on information and problem-solving
  - Formal and professional responses
  - Perfect for work and learning

- `/role_girlfriend` - Switch to girlfriend mode
  - Warm and affectionate responses
  - Emotional support and companionship
  - Casual and friendly conversation

### Search Features
- `/search [query]` - Search and analyze web results
- `/on_search` - Enable automatic web search
- `/off_search` - Disable automatic web search

### Image Features
- `/image [URL]` - Analyze an image in detail
- `/search_image [URL]` - Search information about an image
- `/generate [prompt]` - Create AI artwork

## 💾 Memory Management

The bot includes a sophisticated memory management system:

- Default limit of 50 messages per user
- Automatic pruning of old messages
- Persistent storage across restarts
- Individual user memory spaces
- Command-based memory control

## 🔧 Customization

The bot can be customized by:

1. Modifying `config.py` settings
2. Adjusting personality prompts
3. Changing memory limits
4. Customizing response formatting

## 🛡️ Security

- Environment variables for sensitive data
- No storage of sensitive user information
- Regular memory cleanup
- Rate limiting on API calls
- Error handling and logging

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [python-telegram-bot](https://python-telegram-bot.org/) for the Telegram bot framework
- [Groq AI](https://groq.com) for the AI capabilities
- [DuckDuckGo](https://duckduckgo.com) for web search functionality

## 📞 Support

For support, please:
1. Check the [issues](https://github.com/chamika1/ai_chat_bot/issues) page
2. Create a new issue if needed
3. Join our [Telegram group](https://t.me/your_support_group) (optional)

---

Made with ❤️ by [Chamika](https://github.com/chamika1) 