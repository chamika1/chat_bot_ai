from flask import Flask
import asyncio
import threading
from main import TelegramChatBot
import os
from telegram import Update
from telegram.ext import Application

app = Flask(__name__)
bot = None  # Global bot instance

@app.route('/')
def home():
    return 'Bot is running', 200

@app.route('/health')
def health():
    return 'OK', 200

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

async def init_bot():
    """Initialize the bot asynchronously"""
    global bot
    telegram_token = "7718837777:AAGhYBlLK2Ot7iiIkFcNUApBUjeYI-U86dE"
    groq_api_key = "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"
    
    bot = TelegramChatBot(telegram_token, groq_api_key)
    await bot.run_async()

def run_bot():
    """Run the bot in a new event loop"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(init_bot())
    loop.close()

if __name__ == '__main__':
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True  # Make thread daemon so it exits when main thread exits
    bot_thread.start()
    
    # Run Flask in the main thread
    run_flask() 