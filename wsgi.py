from flask import Flask
import threading
from main import TelegramChatBot

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running', 200

@app.route('/health')
def health():
    return 'OK', 200

def run_bot():
    telegram_token = "7718837777:AAGhYBlLK2Ot7iiIkFcNUApBUjeYI-U86dE"
    groq_api_key = "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"
    
    bot = TelegramChatBot(telegram_token, groq_api_key)
    bot.run()

# Start the bot in a separate thread
bot_thread = threading.Thread(target=run_bot)
bot_thread.start()

if __name__ == '__main__':
    app.run() 