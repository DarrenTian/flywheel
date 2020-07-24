from .utils.config import Config

STOCK_LIST = Config.get_list('STOCK_LIST', [
    'AAPL', 'AMZN', 'BABA', 'CRM', 'EBAY', 'FB', 'GOOG', 'INTC',
    'MSFT', 'NIKE', 'PINS', 'PYPL', 'RKUNY', 'SBUX', 'TSLA', 'TWTR', 'UBER'
])
TZ = Config.get('TZ', 'Asia/Shanghai')
REDIS_URI = Config.get('REDIS_URI', 'redis://localhost:6379')
DB_URL = Config.get('DB_URL', 'mysql://root:123456@127.0.0.1:3306/flywheel')
