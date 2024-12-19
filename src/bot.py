import logging
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import Config
from price_fetcher import PriceFetcher

# Add more detailed logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Add an immediate log message
print("Bot is starting...")
logger = logging.getLogger(__name__)
logger.info("Initializing bot...")

# Set up logging to help us track what's happening with our bot
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class CryptoBot:
    def __init__(self):
        """Initialize the bot with configuration and dependencies"""
        # Validate configuration before starting
        Config.validate()
        
        # Initialize the bot application with your token
        self.app = Application.builder().token(Config.TELEGRAM_TOKEN).build()
        
        # Initialize the price fetcher
        self.price_fetcher = PriceFetcher()
        
        # Dictionary to store active price update tasks for each chat
        self.update_tasks = {}

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command - introduce the bot and its features"""
        welcome_message = (
            "👋 Welcome to the Crypto Price Bot!\n\n"
            "I can help you track cryptocurrency prices. Here are my commands:\n"
            "• /startupdate - Start receiving hourly BTC price updates\n"
            "• /stopupdate - Stop receiving price updates\n"
            "• /price - Get current BTC price immediately\n\n"
            "To begin, try the /startupdate command!"
        )
        await update.message.reply_text(welcome_message)

    async def price(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /price command - send current price immediately"""
        price, timestamp = self.price_fetcher.get_bitcoin_price()
        if price:
            message = self._format_price_message(price, timestamp)
            await update.message.reply_text(message)
        else:
            await update.message.reply_text("Sorry, I couldn't fetch the price right now. Please try again later.")

    async def start_updates(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /startupdate command - begin sending periodic updates"""
        chat_id = update.effective_chat.id
        
        # Check if updates are already running for this chat
        if chat_id in self.update_tasks:
            await update.message.reply_text("Price updates are already running! Use /stopupdate to stop them.")
            return
        
        # Start the update task for this chat
        self.update_tasks[chat_id] = asyncio.create_task(
            self._send_periodic_updates(chat_id)
        )
        
        await update.message.reply_text("Starting hourly BTC price updates! 📊")

    async def stop_updates(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /stopupdate command - stop sending periodic updates"""
        chat_id = update.effective_chat.id
        
        # Check if updates are running for this chat
        if chat_id in self.update_tasks:
            # Cancel the update task
            self.update_tasks[chat_id].cancel()
            del self.update_tasks[chat_id]
            await update.message.reply_text("Stopped BTC price updates! ⏹️")
        else:
            await update.message.reply_text("No price updates are currently running!")

    def _format_price_message(self, price: float, timestamp: datetime) -> str:
        """Format the price update message with a consistent style"""
        return (
            "🔔 BTC Price Update\n"
            f"💰 ${price:,.2f} USD\n"
            f"⏰ {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    async def _send_periodic_updates(self, chat_id: int):
        """Send periodic price updates to a specific chat"""
        while True:
            try:
                # Fetch and send the current price
                price, timestamp = self.price_fetcher.get_bitcoin_price()
                if price:
                    message = self._format_price_message(price, timestamp)
                    await self.app.bot.send_message(chat_id=chat_id, text=message)
                
                # Wait for the configured interval
                await asyncio.sleep(Config.UPDATE_INTERVAL)
                
            except asyncio.CancelledError:
                # Handle cancellation gracefully
                logger.info(f"Stopping price updates for chat {chat_id}")
                break
            except Exception as e:
                logger.error(f"Error in price update loop: {e}")
                await asyncio.sleep(60)  # Wait a minute before retrying

    def run(self):
        """Start the bot and set up command handlers"""
        # Register command handlers
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("price", self.price))
        self.app.add_handler(CommandHandler("startupdate", self.start_updates))
        self.app.add_handler(CommandHandler("stopupdate", self.stop_updates))
        
        # Start the bot
        logger.info("Starting bot...")
        self.app.run_polling()

if __name__ == "__main__":
    # Create and run the bot
    bot = CryptoBot()
    bot.run()