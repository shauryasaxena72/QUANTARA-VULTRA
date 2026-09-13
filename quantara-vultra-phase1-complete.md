# Quantara Vultra — Phase 1: Complete Step-by-Step Guide (Enhanced & Detailed)

*Version: 1.2 — Comprehensive technical walkthrough with troubleshooting guidance*

---

## STEP 1: Verify Your Environment

### Why This Matters
Python version compatibility is critical. The project relies on `hmmlearn` (for statistical modeling) and modern `asyncio` features. Older Python versions (<3.10) may lack required C extensions or have incompatible async libraries.

### Actions
```bash
python --version
```

**Expected:** `Python 3.10.12` or newer (3.11+ preferred for performance).

**Troubleshooting:**
- If you see `Python 3.7` or older: Download the latest stable release from python.org.
- If `python` command not found: Add Python to PATH or use `where python` (Windows) / `which python` (Linux/Mac).
- If `ModuleNotFoundError` occurs later: Re-run `python -m pip install --upgrade pip setuptools wheel` and reinstall dependencies.

**Common Pitfall:** Some systems have multiple Python installations. Ensure you're using the one associated with your IDE/terminal.

---

## STEP 2: Create Project & Virtual Environment

### Why Virtual Environments Matter
Isolating dependencies prevents version conflicts between projects. Without a venv, `pip install` globally can overwrite packages needed by other work, causing silent failures downstream.

### Actions
```bash
# Create project directory
mkdir quantara-vultra
cd quantara-vultra

# Create virtual environment
python -m venv venv
```

**Activation (by OS):**
- **macOS/Linux:** `source venv/bin/activate`
- **Windows PowerShell:** `venv\Scripts\Activate.ps1`
- **Windows CMD:** `venv\Scripts\activate.bat`

**Verification:** Your terminal prompt should show `(venv)` at the start.

**Best Practice:** Delete and recreate the venv periodically to catch corrupted environments early.

---

## STEP 3: Install Dependencies

### Required Packages
| Package | Purpose |
|---------|----------|
| `ccxt` | Cryptocurrency exchange API library (Binance, Coinbase, Alpa) |
| `pandas` | Data manipulation for candle/time-series analysis |
| `numpy` | Numerical computations (stats, math) |
| `hmmlearn` | Hidden Markov Model algorithms for signal extraction |
| `python-dotenv` | Load environment variables from `.env` file |

### Installation Command
```bash
pip install ccxt pandas numpy hmmlearn python-dotenv
```

### Testing the Installation
```bash
python -c "import ccxt, pandas, numpy, hmmlearn, dotenv; print('All imports OK')"
```

**Expected Output:** `All imports OK`

**Troubleshooting:**
- If you get `ModuleNotFoundError` for any package: The installation failed silently. Run `pip install <missing_package>` individually and check the full error traceback.
- If `hmmlearn` fails due to missing compiled extensions: Ensure you have the correct compiler tools (CMake, Fortran) installed on your system.

---

## STEP 4: Build Folder Structure

### Directory Layout
```
quantara-vultra/
├── config/              # Configuration files (settings.py)
├── adapters/            # Exchange adapters (CCXT wrappers)
│   └── schema.py        # Candle data model
├── data/                # Database & storage
│   ├── storage.py       # SQLite persistence
│   └── logs/            # Log files (created at runtime)
├── features/            # Feature engineering (future)
├── regime/              # Market regime detection
├── strategies/          # Trading strategies
│   └── base_strategy.py # Abstract strategy interface
├── allocator/           # Position sizing & risk management
├── risk/               # Risk calculation logic
├── orchestrator/        # Main workflow coordinator
├── logs/               # Application logs
├── scripts/            # Utility scripts
└── requirements.txt    # Dependency list
```

### Creating Directories
```bash
mkdir -p config adapters data features regime strategies allocator risk execution orchestrator logs validation scripts
```

### Creating `__init__.py` Files
```bash
touch adapters/__init__.py
mkdir -p data && touch data/__init__.py
mkdir -p features && touch features/__init__.py
mkdir -p regime && touch regime/__init__.py
mkdir -p strategies && touch strategies/__init__.py
mkdir -p allocator && touch allocator/__init__.py
mkdir -p risk && touch risk/__init__.py
mkdir -p orchestrator && touch orchestrator/__init__.py
mkdir -p logs && touch logs/__init__.py
```

**Why `__init__.py` is Critical:** Without these files, Python doesn't recognize directories as packages. Attempting `from adapters.schema import Candle` would raise `ModuleNotFoundError`.

---

## STEP 5: Secure Secret Management

### `.env` File Creation
Place this in the project root (same level as `requirements.txt`):

```bash
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_secret_here
COINBASE_API_KEY=your_coinbase_api_key_here
COINBASE_API_SECRET=your_coinbase_secret_here
ALPACA_API_KEY=your_alpaca_api_key_here
ALPACA_API_SECRET=your_alpaca_secret_here
```

**Security Notes:**
- Never commit `.env` to version control (add to `.gitignore`).
- Use strong, unique keys for each exchange.
- Rotate keys regularly.
- Consider using a secrets manager (AWS Secrets Manager, HashiCorp Vault) in production.

### `.gitignore` Entry
```
venv/
.env
__pycache__/
*.db
*.pyc
logs/
```

**Critical:** Missing `.gitignore` for `.env` exposes API keys in public repositories — bots can scrape them and drain funds.

---

## STEP 6: Configuration File

### `config/settings.py` — Full Implementation

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env into os.environ

class Settings:
    # Exchange credentials (loaded from .env)
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
    COINBASE_API_KEY = os.getenv("COINBASE_API_KEY")
    COINBASE_API_SECRET = os.getenv("COINBASE_API_SECRET")
    ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
    ALPACA_API_SECRET = os.getenv("ALPACA_API_SECRET")

    # Timeframes
    TIMEFRAMES = ["1m", "15m", "4h"]

    # Risk limits (placeholders — tune for your strategy)
    MIN_CONFIDENCE_THRESHOLD = 0.6      # Minimum confidence for signals
    MAX_POSITION_SIZE_PCT = 0.02        # Max 2% of capital per position
    MAX_DAILY_DRAWNOW_PCT = 0.05       # Stop if down 5% in a day

    # Storage
    DB_PATH = "logs/quantara.db"

settings = Settings()
```

### Testing the Configuration
```bash
python -c "from config.settings import settings; print(settings.TIMEFRAMES)"
```

**Expected Output:** `['1m', '15m', '4h']`

**Validation Tips:**
- Verify all environment variables are present in `.env` before running.
- Check that `DB_PATH` points to an existing or writable directory.
- Ensure `TIMEFRAMES` align with your strategy’s data frequency.

---

## STEP 7: Data Schema (Candle Model)

### `adapters/schema.py` — Complete Implementation

```python
from dataclasses import dataclass
from typing import Literal

Timeframe = Literal["1m", "15m", "4h"]

@dataclass
class Candle:
    exchange: str
    pair: str
    timeframe: Timeframe
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float

    def to_dict(self) -> dict:
        return {
            "exchange": self.exchange,
            "pair": self.pair,
            "timeframe": self.timeframe,
            "timestamp": self.timestamp,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
        }
```

### Testing Immediately
```bash
python -c "
from adapters.schema import Candle
c = Candle(
    exchange='binance',
    pair='BTC/USDT',
    timeframe='1m',
    timestamp=1234567890,
    open=50000.0,
    high=50100.0,
    low=49900.0,
    close=50050.0,
    volume=12.5
)
print(c)
print(c.to_dict())
```

**Expected Output:**
```
Candle(exchange='binance', pair='BTC/USDT', ...)
{
    \"exchange\": \"binance\", \"pair\": \"BTC/USDT\", \"timeframe\": \"1m\", \"timestamp\": 1234567890, \"open\": 50000.0, \"high\": 50100.0, \"low\": 49900.0, \"close\": 50050.0, \"volume\": 12.5
}
```

**Why This Matters:** The `to_dict()` method ensures consistent serialization for database insertion and API payloads.

---

## STEP 8: Base Adapter Interface

### `adapters/base_adapter.py` — Complete Implementation

```python
from abc import ABC, abstractmethod
from typing import Callable, Awaitable
from adapters.schema import Candle, Timeframe

class BaseAdapter(ABC):
    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to exchange API."""
        ...

    @abstractmethod
    async def subscribe_candles(
        self, pair: str, timeframe: Timeframe,
        callback: Callable[[Candle], Awaitable[None]],
    ) -> None:
        """Subscribe to candlestick updates."""
        ...

    @abstractmethod
    async def fetch_historical(
        self, pair: str, timeframe: Timeframe, since: int, limit: int
    ) -> list[Candle]:
        """Fetch historical candle data."""
        ...

    @abstractmethod
    async def place_order(
        self, pair: str, side: str, size: float
    ) -> dict:
        """Place a market order."""
        ...

    @abstractmethod
    def get_available_pairs(self) -> list[str]:
        """Return list of supported trading pairs."""
        ...
```

### Testing the Contract Enforcement
```bash
python -c "
from adapters.base_adapter import BaseAdapter

class IncompleteAdapter(BaseAdapter):
    pass  # Deliberately empty

try:
    IncompleteAdapter()
    print('ERROR: Should have failed!')
except TypeError as e:
    print('Correctly blocked incomplete adapter:', e)
"`

**Expected Output:** `Correctly blocked incomplete adapter: Can't instantiate abstract class IncompleteAdapter...`

**Key Takeaway:** This proves the interface is enforced — any adapter forgetting a method will fail immediately rather than silently breaking.

---

## STEP 9: Base Strategy Interface

### `strategies/base_strategy.py` — Complete Implementation

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal
import pandas as pd

Direction = Literal["long", "short", "flat"]

@dataclass
class Signal:
    direction: Direction
    confidence: float

class BaseStrategy(ABC):
    @abstractmethod
    def generate_signal(
        self, candles_15min: pd.DataFrame, candles_1min: pd.DataFrame
    ) -> Signal:
        """Generate a trading signal based on price action."""
        ...
```

### Quick Sanity Test
```bash
python -c "
from strategies.base_strategy import BaseStrategy, Signal
import pandas as pd

class DummyStrategy(BaseStrategy):
    def generate_signal(self, candles_15min, candles_1min):
        return Signal(direction='long', confidence=0.75)

s = DummyStrategy()
result = s.generate_signal(pd.DataFrame(), pd.DataFrame())
print(result)
"`

**Expected Output:** `Signal(direction='long', confidence=0.75)`

**Design Principle:** The abstraction separates strategy logic from data sources, enabling easy swapping of strategies (e.g., trend-following vs. mean-reversion).

---

## STEP 10: Storage Layer

### `data/storage.py` — Complete Implementation

```python
import sqlite3
from config.settings import settings
from adapters.schema import Candle

def init_db():
    conn = sqlite3.connect(settings.DB_PATH)
    cursor = conn.cursor()
    
    # Candles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candles (
            exchange TEXT NOT NULL,
            pair TEXT NOT NULL,
            timeframe TEXT NOT NULL,
            timestamp INTEGER NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume REAL NOT NULL,
            PRIMARY KEY (exchange, pair, timeframe, timestamp)
        )
    """)
    
    # Decision log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS decision_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER NOT NULL,
            exchange TEXT NOT NULL,
            pair TEXT NOT NULL,
            regime_probs TEXT,
            strategy_signals TEXT,
            allocation TEXT,
            risk_gate_decision TEXT,
            executed BOOLEAN,
            outcome REAL
        )
    """)
    
    conn.commit()
    conn.close()

def save_candle(candle: Candle):
    conn = sqlite3.connect(settings.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO candles
        (exchange, pair, timeframe, timestamp, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (candle.exchange, candle.pair, candle.timeframe, candle.timestamp,
          candle.open, candle.high, candle.low, candle.close, candle.volume))
    conn.commit()
    conn.close()

def get_candle_count() -> int:
    conn = sqlite3.connect(settings.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM candles")
    count = cursor.fetchone()[0]
    conn.close()
    return count
```

### Initialization Script
```python
# scripts/init_db.py
from data.storage import init_db

init_db()
print("Database initialized.")
```

**Running Commands:**
```bash
# Initialize database
python scripts/init_db.py

# Insert a sample candle
python -c "
from data.storage import save_candle
from adapters.schema import Candle

c = Candle(
    exchange='binance',
    pair='BTC/USDT',
    timeframe='1m',
    timestamp=1234567890,
    open=50000.0,
    high=50100.0,
    low=49900.0,
    close=50050.0,
    volume=12.5
)
save_candle(c)
print('Candles in DB:', get_candle_count())
"
```

**Expected Outputs:**
- `Database initialized.`
- `Candles in DB: 1`

**Duplicate Insert Safety:** Using `INSERT OR REPLACE` ensures that replaying historical data won't create duplicates — essential for reprocessing after reconnections.

---

## STEP 11: Common Errors & Debugging Guide

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: No module named 'adapters'` | Missing `__init__.py` in a package directory | Add empty `__init__.py` to the affected folder |
| `TypeError: Can't instantiate abstract class` | Subclass forgot to implement an abstract method | Review the abstract base class and ensure all `@abstractmethod` are implemented |
| `sqlite3.OperationalError: unable to open database file` | `logs/` directory doesn't exist | Run `mkdir -p logs` before initializing the DB |
| `ImportError: cannot import name 'Settings'` | Running from wrong directory or `.env` not loaded | Ensure you're in the project root and `load_dotenv()` is called |
| `AttributeError: 'Candle' object has no attribute 'to_dict'` | Schema class not properly defined | Verify `adapters/schema.py` is in the Python path |

### Debugging Tips
1. **Always run from project root** when importing modules.
2. **Print the exception traceback** — it usually points to the exact line.
3. **Use `python -c "import module"`** to test individual imports.
4. **Check file permissions** — some OSes restrict writes to certain directories.

---

## STEP 12: Final Phase 1 Verification

Run all tests in sequence to confirm Phase 1 completion:

```bash
# 1. Settings & configuration
python -c "from config.settings import settings; print('Settings OK:', settings.TIMEFRAMES)"

# 2. Schema validation
python -c "from adapters.schema import Candle; print('Schema OK')"

# 3. Adapter interface enforcement
python -c "
from adapters.base_adapter import BaseAdapter

class IncompleteAdapter(BaseAdapter):
    pass

try:
    IncompleteAdapter()
    print('FAIL: Should have raised TypeError')
except TypeError as e:
    print('PASS: Correctly blocked incomplete adapter')
"

# 4. Strategy interface
python -c "
from strategies.base_strategy import BaseStrategy, Signal
import pandas as pd

class DummyStrategy(BaseStrategy):
    def generate_signal(self, _, _):
        return Signal(direction='long', confidence=0.75)

s = DummyStrategy()
result = s.generate_signal(pd.DataFrame(), pd.DataFrame())
print('Strategy OK:', result)
"

# 5. Database initialization
python scripts/init_db.py

# 6. Data insertion test
python -c "
from data.storage import save_candle, get_candle_count
from adapters.schema import Candle

c = Candle(
    exchange='binance',
    pair='BTC/USDT',
    timeframe='1m',
    timestamp=1234567890,
    open=50000.0,
    high=50100.0,
    low=49900.0,
    close=50050.0,
    volume=12.5
)
save_candle(c)
print('Candles in DB:', get_candle_count())
"
```

**Success Criteria:** All six commands above should execute without errors and produce the expected outputs. If any step fails, consult the "Common Errors" table for targeted fixes.

---

## Summary

Phase 1 is complete when:
- ✅ Python ≥3.10 is installed
- ✅ Virtual environment is activated
- ✅ All dependencies are installed and importable
- ✅ Folder structure is correctly organized with `__init__.py` files
- ✅ `.env` contains placeholder credentials (never commit real keys)
- ✅ Configuration loads correctly (`settings.TIMEFRAMES` accessible)
- ✅ Schema model works (`Candle` object serializes properly)
- ✅ Abstract interfaces enforce contracts (incomplete adapters/strategies are rejected)
- ✅ Database initializes and accepts data (`get_candle_count()` returns >0)

Once verified, proceed to Phase 2 (exchange integrations, trading logic, and live testing).
