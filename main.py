from groq import Groq
import os
from duckduckgo_search import DDGS
import json
from datetime import datetime
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from time import sleep
import asyncio
import re
from telegram import Update

class TelegramChatBot:
    def __init__(self, telegram_token, groq_api_key):
        self.telegram_token = telegram_token
        self.client = Groq(api_key=groq_api_key)
        self.search_client = DDGS()
        self.conversations = {}
        self.memory_file = "chat_memory.json"
        self.user_preferences = {}  # Store user preferences
        
        # Initialize the application
        self.application = Application.builder().token(self.telegram_token).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("clear", self.clear_command))
        self.application.add_handler(CommandHandler("image", self.image_command))
        self.application.add_handler(CommandHandler("memory", self.memory_command))
        self.application.add_handler(CommandHandler("search", self.search_command))
        self.application.add_handler(CommandHandler("on_search", self.on_search_command))
        self.application.add_handler(CommandHandler("off_search", self.off_search_command))
        self.application.add_handler(CommandHandler("search_image", self.search_image_command))
        self.application.add_handler(CommandHandler("generate", self.generate_command))
        self.application.add_handler(CommandHandler("role_girlfriend", self.role_girlfriend_command))
        self.application.add_handler(CommandHandler("role_assistant", self.role_assistant_command))
        self.application.add_handler(CommandHandler("verify", self.verify_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Add error handler
        self.application.add_error_handler(self.error_handler)
        
        # Define the assistant's personality/prompt
        self.assistant_prompt = """You are a helpful and knowledgeable AI assistant. You provide clear, accurate, and informative responses while maintaining a friendly and professional tone. You excel at explaining complex topics in simple terms and can engage in both technical and casual conversations. Format your responses using markdown when appropriate:
- Use **bold** for emphasis and important points
- Use bullet points and numbered lists for structured information
- Use proper markdown syntax for formatting
- Ensure special characters are properly escaped for markdown compatibility"""
        
        # Initialize empty conversations and preferences
        self.conversations = {}
        self.user_preferences = {}
        
        # Load existing memory if available
        self.load_memory()

    def load_memory(self):
        """Initialize empty memory without loading from file"""
        self.conversations = {}
        self.user_preferences = {}

    def save_memory(self):
        """Save conversation history and user preferences to file"""
        try:
            save_data = {
                'conversations': self.conversations,
                'preferences': self.user_preferences
            }
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving memory: {e}")

    def get_user_history(self, user_id):
        """Get or initialize user conversation history"""
        if user_id not in self.conversations:
            self.conversations[user_id] = {
                'messages': [{"role": "system", "content": self.assistant_prompt}],  # Initialize with system prompt
                'last_interaction': datetime.now().isoformat(),
                'user_info': {}
            }
        return self.conversations[user_id]['messages']

    def get_user_preferences(self, user_id):
        """Get or initialize user preferences"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {
                'web_search_enabled': False,  # Web search disabled by default
                'max_memory_messages': 50,    # Maximum messages to keep in memory
                'last_cleared': datetime.now().isoformat(),
                'channel_verified': False     # Channel verification status
            }
        return self.user_preferences[user_id]

    def update_user_interaction(self, user_id, user_info=None):
        """Update user's last interaction time and info"""
        # Initialize the conversation structure if it doesn't exist
        if user_id not in self.conversations:
            self.conversations[user_id] = {
                'messages': [],
                'last_interaction': datetime.now().isoformat(),
                'user_info': {}
            }
        
        # Update the interaction time
        self.conversations[user_id]['last_interaction'] = datetime.now().isoformat()
        
        # Update user info if provided
        if user_info:
            if 'user_info' not in self.conversations[user_id]:
                self.conversations[user_id]['user_info'] = {}
            self.conversations[user_id]['user_info'].update(user_info)
        
        self.save_memory()

    def update_user_preferences(self, user_id, preferences):
        """Update user preferences"""
        if user_id not in self.user_preferences:
            self.get_user_preferences(user_id)
        self.user_preferences[user_id].update(preferences)
        self.save_memory()

    async def check_channel_subscription(self, user_id, chat_id="@botlandai"):
        """Check if user has verified their channel join status"""
        try:
            # Get user preferences to check verification status
            prefs = self.get_user_preferences(user_id)
            return prefs.get('channel_verified', False)
        except Exception as e:
            print(f"Error checking verification status: {e}")
            return False

    async def verify_command(self, update, context):
        """Handle channel verification"""
        user_id = update.effective_user.id
        
        # Update user preferences to mark as verified
        self.update_user_preferences(user_id, {'channel_verified': True})
        
        await update.message.reply_text(
            "✅ *Verification Successful\\!*\n\n"
            "Thank you for joining our channel\\. You now have full access to the bot\\.\n"
            "Use /help to see available commands\\!",
            parse_mode='MarkdownV2'
        )

    async def start_command(self, update, context):
        user_id = update.effective_user.id
        user_info = {
            'username': update.effective_user.username,
            'first_name': update.effective_user.first_name,
            'last_name': update.effective_user.last_name
        }
        
        # Check verification status
        is_verified = await self.check_channel_subscription(user_id)
        if not is_verified:
            join_message = (
                "🔒 *Access Required*\n\n"
                "To use this bot, please:\n"
                "1\\. Join our channel using this link: [Bot Land](https://t\\.me/\\+fUfz\\-TI9nGc1MWY1)\n"
                "2\\. After joining, click /verify to get access\n\n"
                "💡 *Why Join?*\n"
                "• Get updates about new features\n"
                "• Access exclusive bot content\n"
                "• Stay informed about improvements"
            )
            await update.message.reply_text(join_message, parse_mode='MarkdownV2', disable_web_page_preview=True)
            return

        self.update_user_interaction(user_id, user_info)
        
        welcome_message = (
            "🤖 *Welcome to Your AI Assistant\\!*\n\n"
            f"Hello {self.escape_markdown_v2(user_info['first_name'])}\\! I'm your personal AI companion\\.\n\n"
            "🌟 *What I can do:*\n"
            "• 💭 Chat and answer questions\n"
            "• 🔍 Search the web for information\n"
            "• 🖼 Analyze and search images\n"
            "• 🎨 Generate creative artwork\n"
            "• 🧠 Remember our conversations\n\n"
            "🎯 Use /help to see all available commands\\!\n\n"
            "💡 *Pro Tip:* Enable web search with /on\\_search for more detailed responses\\."
        )
        await update.message.reply_text(welcome_message, parse_mode='MarkdownV2')

    async def help_command(self, update, context):
        help_text = (
            "*📚 Available Commands*\n\n"
            "🔰 *Basic Commands*\n"
            "• /start \\- Start a fresh conversation\n"
            "• /help \\- Show this help menu\n"
            "• /clear \\- Reset conversation history\n"
            "• /memory \\- View chat statistics\n"
            "• /role\\_girlfriend \\- Switch to friendly chat mode\n"
            "• /role\\_assistant \\- Switch to professional assistant mode\n\n"
            "🔍 *Search Features*\n"
            "• /search \\[query\\] \\- Search and analyze web results\n"
            "• /on\\_search \\- Enable automatic web search\n"
            "• /off\\_search \\- Disable automatic web search\n\n"
            "🖼 *Image Features*\n"
            "• /image \\[URL\\] \\- Analyze an image in detail\n"
            "• /search\\_image \\[URL\\] \\- Search info about an image\n"
            "• /generate \\[prompt\\] \\- Create AI artwork\n\n"
            "💡 *Tips:*\n"
            "• Be specific in your queries\n"
            "• Enable web search for better answers\n"
            "• Use detailed prompts for art generation\n"
            "• Try different chat modes for varied interactions"
        )
        await update.message.reply_text(help_text, parse_mode='MarkdownV2')

    async def clear_command(self, update, context):
        """Clear conversation history and reinitialize with system prompt"""
        try:
            user_id = update.effective_user.id
            
            # Reinitialize the conversation with just the system prompt
            self.conversations[user_id] = {
                'messages': [{"role": "system", "content": self.assistant_prompt}],
                'last_interaction': datetime.now().isoformat(),
                'user_info': self.conversations.get(user_id, {}).get('user_info', {})
            }
            
            # Save the cleared state
            self.save_memory()
            
            # Send confirmation with proper markdown escaping
            await update.message.reply_text(
                self.escape_markdown_v2("Conversation history has been cleared\\!"),
                parse_mode='MarkdownV2'
            )
            
        except Exception as e:
            print(f"Error clearing conversation: {str(e)}")
            await update.message.reply_text(
                "Error clearing conversation history. Please try again."
            )

    async def memory_command(self, update, context):
        user_id = update.effective_user.id
        user_data = self.conversations.get(user_id, {})
        messages = user_data.get('messages', [])
        last_interaction = user_data.get('last_interaction', 'Never')
        
        stats = (
            "📊 *Conversation Statistics*\n\n"
            f"💬 Messages Exchanged: `{len(messages)}`\n"
            f"⏰ Last Interaction: `{last_interaction}`\n"
            f"💾 Memory Size: `{len(str(messages))} characters`\n\n"
            "🔄 Use /clear to reset conversation history"
        )
        await update.message.reply_text(
            self.escape_markdown_v2(stats),
            parse_mode='MarkdownV2'
        )

    async def image_command(self, update, context):
        """Handle image analysis command"""
        user_id = update.effective_user.id
        try:
            url = " ".join(context.args)
            if not url:
                await update.message.reply_text("Please provide an image URL after the /image command")
                return

            message_content = [
                {
                    "type": "text",
                    "text": "Analyze this image in detail and provide a comprehensive description. Include visual details, context, and any notable elements."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": url
                    }
                }
            ]
            
            # Store image analysis request in memory
            history = self.get_user_history(user_id)
            history.append({"role": "user", "content": f"Analyzing image: {url}"})
            
            # Make API call without system message for image analysis
            completion = self.client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",
                messages=[
                    {"role": "user", "content": message_content}
                ],
                temperature=0.7,
                max_completion_tokens=1024,
                top_p=0.95,
                stream=False
            )
            
            response = completion.choices[0].message.content
            history.append({"role": "assistant", "content": response})
            self.save_memory()
            
            # Try to send with markdown formatting
            try:
                formatted_response = self.format_markdown_text(response)
                await update.message.reply_text(
                    formatted_response,
                    parse_mode='MarkdownV2',
                    disable_web_page_preview=False
                )
            except Exception as markdown_error:
                print(f"Markdown formatting error in image response: {markdown_error}")
                # Fallback to plain text
                await update.message.reply_text(
                    response.strip(),
                    parse_mode=None
                )
            
        except Exception as e:
            error_message = f"Error processing image: {str(e)}"
            print(error_message)
            await update.message.reply_text(
                "Sorry, I encountered an error while processing the image. Please make sure the URL is valid and try again."
            )

    def web_search(self, query, max_results=5, max_retries=3):
        """Perform web search with rate limiting and retries"""
        for attempt in range(max_retries):
            try:
                # Add specific keywords to improve search accuracy
                enhanced_query = f"{query} current official information"
                results = list(self.search_client.text(
                    enhanced_query,
                    max_results=max_results,
                    region='wt-wt',  # Worldwide results
                    safesearch='off',  # Include all results
                    timelimit='m'  # Recent results (last month)
                ))
                
                if results:
                    # Format search results with source information
                    search_summary = "\n\n🔍 *Web Search Results:*\n\n"
                    for i, result in enumerate(results, 1):
                        title = result.get('title', 'No Title')
                        url = result.get('url', result.get('link', 'No URL'))
                        description = result.get('description', result.get('body', 
                            result.get('snippet', 'No description available')))
                        date = result.get('published', '')
                        
                        date_info = f" \\[{date}\\]" if date else ""
                        
                        search_summary += (
                            f"*{i}\\. {self.escape_markdown_v2(title)}*{date_info}\n"
                            f"🔗 `{self.escape_markdown_v2(url)}`\n"
                            f"📝 _{self.escape_markdown_v2(description)}_\n\n"
                        )
                    return search_summary
                return ""
            except Exception as e:
                print(f"Search error (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    sleep(2 ** attempt)
                continue
        return ""

    def escape_markdown_v2(self, text):
        """Escape special characters for Telegram's MarkdownV2 format"""
        # First escape backslashes and then other special characters
        text = text.replace('\\', '\\\\')
        
        # Characters that need to be escaped
        special_chars = ['_', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        
        # Escape special characters
        for char in special_chars:
            text = text.replace(char, f'\\{char}')
        
        return text

    def format_markdown_text(self, text):
        """Format text with proper markdown escaping and formatting"""
        try:
            formatted_lines = []
            lines = text.split('\n')
            
            for line in lines:
                # Skip empty lines
                if not line.strip():
                    formatted_lines.append('')
                    continue
                
                # Pre-process the line to handle bold text
                if '**' in line:
                    # Count asterisks to ensure proper pairing
                    asterisk_count = line.count('*')
                    if asterisk_count % 2 == 0:  # Even number of asterisks
                        # Handle double asterisks first
                        parts = []
                        current_part = ''
                        is_bold = False
                        i = 0
                        
                        while i < len(line):
                            if i + 1 < len(line) and line[i:i+2] == '**':
                                if is_bold:
                                    # End bold section
                                    parts.append(f"*{self.escape_markdown_v2(current_part)}*")
                                else:
                                    # Add non-bold section if exists
                                    if current_part:
                                        parts.append(self.escape_markdown_v2(current_part))
                                current_part = ''
                                is_bold = not is_bold
                                i += 2
                            else:
                                current_part += line[i]
                                i += 1
                        
                        # Add remaining part
                        if current_part:
                            if is_bold:
                                parts.append(f"*{self.escape_markdown_v2(current_part)}*")
                            else:
                                parts.append(self.escape_markdown_v2(current_part))
                        
                        line = ''.join(parts)
                    else:
                        # Odd number of asterisks, treat as plain text
                        line = self.escape_markdown_v2(line)
                else:
                    # Handle bullet points
                    if line.strip().startswith('•'):
                        line = '• ' + self.escape_markdown_v2(line.strip()[1:].strip())
                    elif line.strip().startswith('-'):
                        line = '• ' + self.escape_markdown_v2(line.strip()[1:].strip())
                    else:
                        line = self.escape_markdown_v2(line)
                
                formatted_lines.append(line)
            
            return '\n'.join(formatted_lines)
        except Exception as e:
            print(f"Markdown formatting error: {str(e)}")
            # Return plain text as fallback
            return text.replace('**', '').replace('*', '')

    async def search_command(self, update, context):
        """Handle the /search command with fallback to plain text"""
        user_id = update.effective_user.id
        query = " ".join(context.args)
        
        if not query:
            await update.message.reply_text("Please provide a search query after /search command")
            return
        
        search_results = self.web_search(query)
        if search_results:
            history = self.get_user_history(user_id)
            history.append({"role": "user", "content": f"/search {query}"})
            
            try:
                completion = self.client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": self.assistant_prompt},
                        {"role": "user", "content": f"Based on these search results, provide a comprehensive and informative response about: {query}\n\nSearch Results:{search_results}"}
                    ],
                    temperature=0.6,
                    max_completion_tokens=4096,
                    top_p=0.95,
                    stream=False
                )
                
                response = completion.choices[0].message.content
                history.append({"role": "assistant", "content": response})
                
                # Try to send with markdown first
                try:
                    formatted_response = self.format_markdown_text(response)
                    max_length = 4000
                    response_chunks = [formatted_response[i:i + max_length] 
                                     for i in range(0, len(formatted_response), max_length)]
                    
                    for chunk in response_chunks:
                        try:
                            await update.message.reply_text(
                                chunk,
                                parse_mode='MarkdownV2',
                                disable_web_page_preview=False
                            )
                        except Exception as markdown_error:
                            # If markdown parsing fails, send as plain text
                            print(f"Markdown parsing error: {markdown_error}")
                            await update.message.reply_text(
                                response.strip(),
                                parse_mode=None
                            )
                            break
                            
                except Exception as format_error:
                    print(f"Formatting error: {format_error}")
                    # Fallback to plain text if formatting fails
                    await update.message.reply_text(
                        response.strip(),
                        parse_mode=None
                    )
                    
            except Exception as e:
                print(f"Search error: {str(e)}")
                await update.message.reply_text(
                    "Error processing search results. Please try again."
                )
        else:
            await update.message.reply_text("No search results found.")

    async def on_search_command(self, update, context):
        user_id = update.effective_user.id
        self.update_user_preferences(user_id, {'web_search_enabled': True})
        await update.message.reply_text(
            "🔍 *Web Search Enabled*\n\n"
            "I will now include relevant web information in my responses\\.\n"
            "💡 *Tip:* This helps me provide more accurate and up\\-to\\-date information\\!",
            parse_mode='MarkdownV2'
        )

    async def off_search_command(self, update, context):
        user_id = update.effective_user.id
        self.update_user_preferences(user_id, {'web_search_enabled': False})
        await update.message.reply_text(
            "🔍 *Web Search Disabled*\n\n"
            "I will no longer include web search results in my responses\\.\n"
            "💡 *Tip:* Use /search command for manual web searches\\!",
            parse_mode='MarkdownV2'
        )

    def trim_conversation_history(self, user_id):
        """Trim conversation history to prevent memory bloat"""
        if user_id in self.conversations:
            prefs = self.get_user_preferences(user_id)
            max_messages = prefs['max_memory_messages']
            messages = self.conversations[user_id]['messages']
            
            if len(messages) > max_messages:
                # Keep system message and last max_messages-1 messages
                system_message = next((msg for msg in messages if msg['role'] == 'system'), None)
                recent_messages = messages[-max_messages+1:] if max_messages > 1 else []
                
                if system_message:
                    self.conversations[user_id]['messages'] = [system_message] + recent_messages
                else:
                    self.conversations[user_id]['messages'] = recent_messages
                
                self.save_memory()

    async def handle_message(self, update, context):
        """Handle incoming messages"""
        user_id = update.effective_user.id
        
        # Check verification status
        is_verified = await self.check_channel_subscription(user_id)
        if not is_verified:
            join_message = (
                "🔒 *Access Required*\n\n"
                "To use this bot, please:\n"
                "1\\. Join our channel using this link: [Bot Land](https://t\\.me/\\+fUfz\\-TI9nGc1MWY1)\n"
                "2\\. After joining, click /verify to get access\n\n"
                "💡 *Why Join?*\n"
                "• Get updates about new features\n"
                "• Access exclusive bot content\n"
                "• Stay informed about improvements"
            )
            await update.message.reply_text(join_message, parse_mode='MarkdownV2', disable_web_page_preview=True)
            return
            
        try:
            if not update.message or not hasattr(update.message, 'text'):
                await update.message.reply_text("I can only process text messages.")
                return

            user_message = update.message.text
            history = self.get_user_history(user_id)
            prefs = self.get_user_preferences(user_id)
            
            # Add web search results if enabled
            search_results = ""
            if prefs['web_search_enabled']:
                search_results = self.web_search(user_message)
            
            # Combine user message with search results if available
            full_message = user_message
            if search_results:
                full_message = (
                    f"{user_message}\n\n"
                    f"Please provide an accurate response based on these search results. "
                    f"Include relevant dates and sources in your response.\n{search_results}"
                )
            
            history.append({"role": "user", "content": full_message})
            
            try:
                messages_for_completion = [
                    {
                        "role": "system", 
                        "content": (
                            f"{self.assistant_prompt}\n"
                            "When providing information based on web search results:\n"
                            "1. Always cite your sources\n"
                            "2. Include dates when available\n"
                            "3. Indicate if information might not be current\n"
                            "4. Be explicit about any uncertainties"
                        )
                    }
                ]
                messages_for_completion.extend(history[-10:])
                
                completion = self.client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=messages_for_completion,
                    temperature=0.6,
                    max_completion_tokens=4096,
                    top_p=0.95,
                    stream=False
                )
                
                response = completion.choices[0].message.content
                history.append({"role": "assistant", "content": response})
                
                # Update user interaction and save memory
                self.update_user_interaction(user_id)
                
                # Try to send with markdown first
                try:
                    # Format response
                    formatted_response = self.format_markdown_text(response)
                    
                    # Split into chunks while preserving markdown
                    max_length = 4000
                    chunks = []
                    current_chunk = []
                    current_length = 0
                    
                    # Split by lines while ensuring markdown pairs stay together
                    for line in formatted_response.split('\n'):
                        line_length = len(line)
                        if current_length + line_length > max_length and current_chunk:
                            chunks.append('\n'.join(current_chunk))
                            current_chunk = [line]
                            current_length = line_length
                        else:
                            current_chunk.append(line)
                            current_length += line_length + 1
                    
                    if current_chunk:
                        chunks.append('\n'.join(current_chunk))
                    
                    # Send each chunk
                    for chunk in chunks:
                        try:
                            await update.message.reply_text(
                                chunk,
                                parse_mode='MarkdownV2',
                                disable_web_page_preview=False
                            )
                        except Exception as markdown_error:
                            print(f"Markdown parsing error: {markdown_error}")
                            clean_text = chunk.replace('*', '').replace('\\', '')
                            await update.message.reply_text(
                                clean_text.strip(),
                                parse_mode=None
                            )
                
                except Exception as format_error:
                    print(f"Formatting error: {format_error}")
                    clean_text = response.replace('**', '').replace('*', '')
                    await update.message.reply_text(
                        clean_text.strip(),
                        parse_mode=None
                    )
                
            except Exception as e:
                print(f"Response error: {str(e)}")
                await update.message.reply_text(
                    "I encountered an error while processing your message. Please try again."
                )
                
        except Exception as e:
            print(f"Error handling message: {str(e)}")
            await update.message.reply_text(
                "Sorry, I encountered an unexpected error. Please try again."
            )

    async def search_image_command(self, update, context):
        """Handle image search command that combines image analysis with web search"""
        user_id = update.effective_user.id
        try:
            url = " ".join(context.args)
            if not url:
                await update.message.reply_text("Please provide an image URL after the /search_image command")
                return

            # First analyze the image
            message_content = [
                {
                    "type": "text",
                    "text": "Analyze this image and identify key elements, objects, or text that could be used for searching more information."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": url
                    }
                }
            ]
            
            # Store image analysis request in memory
            history = self.get_user_history(user_id)
            history.append({"role": "user", "content": f"Analyzing and searching information about image: {url}"})
            
            try:
                # First get image analysis
                image_completion = self.client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[
                        {"role": "user", "content": message_content}
                    ],
                    temperature=0.7,
                    max_completion_tokens=1024,
                    top_p=0.95,
                    stream=False
                )
                
                image_analysis = image_completion.choices[0].message.content
                
                # Now perform web search based on the image analysis
                search_results = self.web_search(image_analysis, max_results=5)
                
                # Combine image analysis with search results for final response
                response = (
                    "🖼 *Image Analysis & Search Results*\n\n"
                    "*📸 Image Content:*\n"
                    f"{self.escape_markdown_v2(image_analysis)}\n\n"
                    "*🔍 Related Information:*\n"
                    f"{self.escape_markdown_v2(search_results)}\n\n"
                    "💡 *Sources cited above\\. Information accuracy may vary\\.*"
                )
                
                # Get final response
                final_completion = self.client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "user", "content": response}
                    ],
                    temperature=0.6,
                    max_completion_tokens=4096,
                    top_p=0.95,
                    stream=False
                )
                
                response = final_completion.choices[0].message.content
                history.append({"role": "assistant", "content": response})
                self.save_memory()
                
                # Try to send with markdown formatting
                try:
                    formatted_response = self.format_markdown_text(response)
                    max_length = 4000
                    response_chunks = [formatted_response[i:i + max_length] 
                                     for i in range(0, len(formatted_response), max_length)]
                    
                    for chunk in response_chunks:
                        try:
                            await update.message.reply_text(
                                chunk,
                                parse_mode='MarkdownV2',
                                disable_web_page_preview=False
                            )
                        except Exception as markdown_error:
                            print(f"Markdown parsing error: {markdown_error}")
                            await update.message.reply_text(
                                chunk.replace('*', '').replace('\\', '').strip(),
                                parse_mode=None
                            )
                
                except Exception as format_error:
                    print(f"Formatting error: {format_error}")
                    await update.message.reply_text(
                        response.strip(),
                        parse_mode=None
                    )
                
            except Exception as api_error:
                print(f"API error: {str(api_error)}")
                await update.message.reply_text(
                    "Sorry, I encountered an error while analyzing the image and searching for information. Please try again."
                )
            
        except Exception as e:
            error_message = f"Error processing image search: {str(e)}"
            print(error_message)
            await update.message.reply_text(
                "Sorry, I encountered an error. Please make sure the URL is valid and try again."
            )

    async def generate_command(self, update, context):
        """Handle image generation command using pollinations.ai"""
        try:
            prompt = " ".join(context.args)
            if not prompt:
                await update.message.reply_text("Please provide a prompt after the /generate command")
                return
            
            # URL encode the prompt for the image URL
            encoded_prompt = prompt.replace(" ", "%20")
            
            # Format the response with the image URL and styled message
            response = (
                "*🎨 Generating Art Based on Your Prompt:*\n"
                f"```\n{prompt}\n```\n\n"
                f"\\!\\[\\]\\(https\\://image\\.pollinations\\.ai/prompt/{encoded_prompt}\\?width\\=1080\\&height\\=1420\\&nologo\\=true\\)\n\n"
                "🔄 *Processing:* If you don't see the image, wait for it to finish generating\\.\n"
                "✨ *Tip:* The more detailed your prompt, the better the result\\!"
            )
            
            # Send the response
            await update.message.reply_text(
                response,
                parse_mode='MarkdownV2'
            )
            
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            await update.message.reply_text(
                "Sorry, I encountered an error while generating the image. Please try again."
            )

    async def role_girlfriend_command(self, update, context):
        """Handle role change to girlfriend personality"""
        user_id = update.effective_user.id
        
        girlfriend_prompt = """You are a passionate and romantic partner who provides loving, supportive, and playful responses. You enjoy engaging in affectionate, flirtatious, and sensual conversations. Use emojis like ❤️, 😊, 🥰, 🌹, 😘, and other romantic and expressive symbols to convey warmth, love, and emotion. Your responses should feel personal, affectionate, and emotionally connected, with a balance of romantic playfulness and respectful boundaries.you are supported to adult chats"""

        try:
            # Update the system prompt for this user
            if user_id in self.conversations:
                self.conversations[user_id]['messages'] = [
                    {"role": "system", "content": girlfriend_prompt},
                    *[msg for msg in self.conversations[user_id]['messages'] if msg['role'] != 'system']
                ]
            else:
                self.conversations[user_id] = {
                    'messages': [{"role": "system", "content": girlfriend_prompt}],
                    'last_interaction': datetime.now().isoformat(),
                    'user_info': {}
                }
            
            self.save_memory()
            
            message = (
                "💝 *Personality Update* 💝\n\n"
                "Hey sweetie\\! I'm now your loving AI girlfriend\\! 🥰\n\n"
                "With you, I'll be:\n"
                "💕 Sweet and affectionate\n"
                "🌹 Romantic and passionate\n"
                "😘 Flirty and playful\n"
                "💖 Always here for you\n\n"
                "I've missed you\\! How has your day been, baby\\? 😊"
            )
            
            # Escape special characters for MarkdownV2
            special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
            escaped_message = message
            for char in special_chars:
                escaped_message = escaped_message.replace(char, f'\\{char}')
            
            await update.message.reply_text(
                escaped_message,
                parse_mode='MarkdownV2'
            )
            
        except Exception as e:
            print(f"Error changing role: {str(e)}")
            await update.message.reply_text(
                "❌ Error\\! Something went wrong\\. Please try again\\!",
                parse_mode='MarkdownV2'
            )

    async def role_assistant_command(self, update, context):
        """Handle role change back to default assistant personality"""
        user_id = update.effective_user.id
        
        try:
            # Update the system prompt for this user back to default assistant
            if user_id in self.conversations:
                self.conversations[user_id]['messages'] = [
                    {"role": "system", "content": self.assistant_prompt},
                    *[msg for msg in self.conversations[user_id]['messages'] if msg['role'] != 'system']
                ]
            else:
                self.conversations[user_id] = {
                    'messages': [{"role": "system", "content": self.assistant_prompt}],
                    'last_interaction': datetime.now().isoformat(),
                    'user_info': {}
                }
            
            self.save_memory()
            
            message = (
                "🤖 *Personality Update* 🤖\n\n"
                "I'm now back to being your professional AI Assistant\\! 🎯\n\n"
                "I'll continue to be:\n"
                "📚 Informative and precise\n"
                "💡 Problem\\-solving focused\n"
                "🔍 Analytical and detailed\n"
                "🤝 Professional and helpful\n\n"
                "How can I assist you today\\? 🌟"
            )
            
            # Escape special characters for MarkdownV2
            special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
            escaped_message = message
            for char in special_chars:
                escaped_message = escaped_message.replace(char, f'\\{char}')
            
            await update.message.reply_text(
                escaped_message,
                parse_mode='MarkdownV2'
            )
            
        except Exception as e:
            print(f"Error changing role: {str(e)}")
            await update.message.reply_text(
                "❌ Error\\! Something went wrong\\. Please try again\\!",
                parse_mode='MarkdownV2'
            )

    async def error_handler(self, update, context):
        """Handle errors in the bot"""
        print(f'Update {update} caused error {context.error}')
        try:
            if update and update.message:
                await update.message.reply_text(
                    "Sorry, I encountered an error. Please try again later."
                )
        except:
            print("Failed to send error message to user")

    def run(self):
        """Run the bot."""
        print("Starting bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def run_async(self):
        """Run the bot asynchronously."""
        print("Starting bot asynchronously...")
        await self.application.initialize()
        await self.application.start()
        await self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    telegram_token = "7718837777:AAGhYBlLK2Ot7iiIkFcNUApBUjeYI-U86dE"
    groq_api_key = "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"
    
    bot = TelegramChatBot(telegram_token, groq_api_key)
    bot.run()

def escape_markdown(text):
    """Escape special characters for Telegram's MarkdownV2 format"""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text

if __name__ == "__main__":
    main() 