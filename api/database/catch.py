from flask_caching import Cache
import os
from dotenv import load_dotenv

load_dotenv()

redis_url = os.environ.get('CACHE_REDIS_URL')

if not redis_url:
    raise ValueError("Redis連線失效")

cache = Cache(config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': redis_url,
    'CACHE_DEFAULT_TIMEOUT': 60
})