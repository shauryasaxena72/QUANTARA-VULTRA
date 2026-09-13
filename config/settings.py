import os
from dotenv import load_dotenv
load_dotenv
class Settings:
    BINANCE_API_KEY=os.getenv("BINANCE_API_KEY")
    BINANCE_API_SECRET=os.getenv("BINANCE_API_SECRET")
    COINBASE_API_KEY=os.getenv("COINBASE_API_KEY")
    COINBASE_API_SECRET=os.getenv("COINBASE_API_SECRET")
    ALPACA_API_KEY=os.getenv("ALPACA_API_KEY")
    ALPACA_API_SECRET=os.getenv("ALPACA_API_SECRET")

    TIMEFRAMES = ["1m","15m","1h","4h"]

    