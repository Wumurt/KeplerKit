import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()  # Загружаем из .env

# уровень логирования или default
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# база данных
DB_CONFIG = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'dbname': os.getenv('DB_NAME'),
    'remote_db_url': os.getenv('REMOTE_DB'),
    # Оставь None если хочешь подключиться к локальному постгресу / сформировать url самостоятельно
}

# местоположение наблюдателя
OBSERVER = {
    'observer_lat': os.getenv('OBSERVER_LAT'),
    'observer_lon': os.getenv('OBSERVER_LON')
}

# ключ к n2yo.com
N2YO_API_KEY = os.getenv('N2YO_API_KEY')

logger.info('Settings successfully loaded')
