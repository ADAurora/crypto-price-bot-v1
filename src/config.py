# src/config.py
import os
from dotenv import load_dotenv

# First, load the environment variables from .env file
print("Loading environment variables...")
load_dotenv()

# Configuration class to manage all settings
class Config:
    # Get Telegram token from environment variables
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    
    # Bot settings
    UPDATE_INTERVAL = 3600  # Update interval in seconds (1 hour)
    
    # Validate configuration
    @classmethod
    def validate(cls):
        if not cls.TELEGRAM_TOKEN:
            raise ValueError(
                "Telegram token not found! "
                "Please make sure you have created a .env file "
                "with your TELEGRAM_TOKEN."
            )

# Now we can check if the token was loaded successfully
print(f"Token loaded: {'YES' if Config.TELEGRAM_TOKEN else 'NO'}")