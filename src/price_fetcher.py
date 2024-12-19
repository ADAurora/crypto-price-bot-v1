# src/price_fetcher.py
import requests
from datetime import datetime

class PriceFetcher:
    def __init__(self):
        # Base URL for CoinGecko API
        self.base_url = "https://api.coingecko.com/api/v3"
    
    def get_bitcoin_price(self):
        """
        Fetches the current Bitcoin price in USD from CoinGecko.
        
        Returns:
            tuple: (price, timestamp) if successful, (None, None) if failed
        """
        try:
            # Construct the API endpoint
            endpoint = f"{self.base_url}/simple/price"
            params = {
                "ids": "bitcoin",
                "vs_currencies": "usd"
            }
            
            # Make the API request
            response = requests.get(endpoint, params=params)
            response.raise_for_status()  # Raises an error for bad status codes
            
            # Extract the price from the response
            price = response.json()["bitcoin"]["usd"]
            timestamp = datetime.now()
            
            return price, timestamp
            
        except Exception as e:
            print(f"Error fetching Bitcoin price: {e}")
            return None, None