from flask import Flask
import asyncio
import threading
from main import TelegramChatBot
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running', 200

@app.route('/health')
def health():
    return 'OK', 200

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def run_bot():
    telegram_token = "7718837777:AAGhYBlLK2Ot7iiIkFcNUApBUjeYI-U86dE"
    groq_api_key = "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"
    
    bot = TelegramChatBot(telegram_token, groq_api_key)
    
    # Create a new event loop for the bot
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Run the bot in the new event loop
    loop.run_until_complete(bot.run_async())

if __name__ == '__main__':
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    
    # Run Flask in the main thread
    run_flask() 