from breeze_connect import BreezeConnect
from dotenv import load_dotenv
import os
import json
import threading
import time

load_dotenv()

class BreezeStreamer:
    def __init__(self):
        self.breeze = BreezeConnect(api_key=os.getenv("API_KEY"))
        self.connected = False
        self.subscriptions = set()
        
        # Initialize with session token if available
        if os.getenv("ACCESS_TOKEN"):
            self.breeze.generate_session(
                api_secret=os.getenv("API_SECRET"),
                session_token=os.getenv("ACCESS_TOKEN")
            )
    
    def connect(self):
        """Connect to WebSocket and start streaming"""
        if not self.connected:
            self.breeze.ws_connect()
            self.connected = True
            
            # Assign callbacks
            self.breeze.on_ticks = self.on_ticks
            self.breeze.on_open = self.on_open
            self.breeze.on_close = self.on_close
            self.breeze.on_error = self.on_error
            
            print("WebSocket connected successfully")
    
    def disconnect(self):
        """Disconnect from WebSocket"""
        if self.connected:
            self.breeze.ws_disconnect()
            self.connected = False
            print("WebSocket disconnected")
    
    def on_ticks(self, ticks):
        print(f"Tick received: {json.dumps(ticks, indent=2)}")
        # Here you can process ticks (store in DB, file, etc.)
    
    def on_open(self, ws):
        print("WebSocket connection opened")
    
    def on_close(self, ws):
        print("WebSocket connection closed")
        self.connected = False
    
    def on_error(self, ws, error):
        print(f"WebSocket error: {error}")
    
    def subscribe(self, exchange_code, stock_code, product_type, 
                 expiry_date=None, strike_price=None, right=None,
                 interval=None, get_market_depth=False, 
                 get_exchange_quotes=True):

        subscription_key = (exchange_code, stock_code, product_type, 
                          expiry_date, strike_price, right)
        
        if subscription_key not in self.subscriptions:
            self.breeze.subscribe_feeds(
                exchange_code=exchange_code,
                stock_code=stock_code,
                expiry_date=expiry_date,
                strike_price=strike_price,
                right=right,
                product_type=product_type,
                get_market_depth=get_market_depth,
                get_exchange_quotes=get_exchange_quotes,
                interval=interval
            )
            self.subscriptions.add(subscription_key)
            print(f"Subscribed to {stock_code} on {exchange_code}")

def start_streaming():
    """Start WebSocket streaming in a separate thread"""
    streamer = BreezeStreamer()
    streamer.connect()
    
    # NSE Cash Market
    streamer.subscribe(
        exchange_code="NSE",
        stock_code="NIFTY",
        product_type="cash"
    )
    
    # NFO Options Market
    streamer.subscribe(
        exchange_code="NFO",
        stock_code="NIFTY",
        expiry_date="13-Feb-2025",
        strike_price="23550",
        right="call",
        product_type="options",
        interval="1minute"
    )
    
    # Keep the connection alive
    while True:
        time.sleep(1)

if __name__ == "__main__":
    start_streaming()