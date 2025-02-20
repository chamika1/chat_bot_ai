from main import app, main
import threading
import os

if __name__ == "__main__":
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=main)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Run Flask app
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000))) 