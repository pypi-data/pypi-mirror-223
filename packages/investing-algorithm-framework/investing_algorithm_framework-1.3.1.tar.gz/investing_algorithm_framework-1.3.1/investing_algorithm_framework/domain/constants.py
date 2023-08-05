# Framework constants
FRAMEWORK_NAME = 'FRAMEWORK_NAME'
ENVIRONMENT = "ENVIRONMENT"
STATELESS = "STATELESS"

# Database Constants
DATABASE_CONFIG = 'DATABASE_CONFIG'
DATABASE_NAME = 'DATABASE_NAME'
DATABASE_TYPE = 'DATABASE_TYPE'
DATABASE_DIRECTORY_PATH = 'DATABASE_DIRECTORY_PATH'
DATABASE_URL = 'DATABASE_URL'
DEFAULT_DATABASE_NAME = "database"

RESOURCE_DIRECTORY = "RESOURCE_DIRECTORY"
LOG_LEVEL = 'LOG_LEVEL'
BASE_DIR = 'BASE_DIR'
SQLALCHEMY_DATABASE_URI = 'SQLALCHEMY_DATABASE_URI'
SQLITE_INITIALIZED = "SQLITE_INITIALIZED"
SQLALCHEMY_INITIALIZED = "SQLALCHEMY_INITIALIZED"


BINANCE = "BINANCE"

IDENTIFIER_QUERY_PARAM = "identifier"
TARGET_SYMBOL_QUERY_PARAM = "target_symbol"
TRADING_SYMBOL_QUERY_PARAM = "trading_symbol"
ORDER_SIDE_QUERY_PARAM = "side"
STATUS_QUERY_PARAM = "status"
POSITION_SYMBOL_QUERY_PARAM = "position"
SYMBOL_QUERY_PARAM = "symbol"
TIME_FRAME_QUERY_PARAM = "time_frame"

RESERVED_IDENTIFIERS = [
    BINANCE
]

BINANCE_API_KEY = "binance_api_key"
BINANCE_SECRET_KEY = "binance_secret_key"

CHECK_PENDING_ORDERS = "CHECK_PENDING_ORDERS"
RUN_STRATEGY = "RUN_STRATEGY"

# Configuration
TRADING_SYMBOL = "TRADING_SYMBOL"
CCXT_ENABLED = "CCXT_ENABLED"
API_KEY = "API_KEY"
SECRET_KEY = "SECRET_KEY"
MARKET = "MARKET"
TRACK_PORTFOLIO_FROM = "TRACK_PORTFOLIO_FROM"
SQLITE_ENABLED = "SQLITE_ENABLED"
PORTFOLIOS = "PORTFOLIOS"
STRATEGIES = "STRATEGIES"
APPLICATION_CONFIGURED = "APPLICATION_CONFIGURED"
ACTION = "ACTION"

DEFAULT_PER_PAGE_VALUE = 10
DEFAULT_PAGE_VALUE = 1
ITEMIZE = 'itemize'
ITEMIZED = 'itemized'
PAGE = 'page'
PER_PAGE = 'per_page'

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
