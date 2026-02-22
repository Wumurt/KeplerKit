# Подключение к PostgreSQL (используя SQLAlchemy)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.settings import DB_CONFIG
import logging

logger = logging.getLogger(__name__)

if DB_CONFIG['remote_db_url'] is None:
    # Строка подключения к локальному постгресу
    DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
else:
    # Строка подключения к удаленному постгресу
    DATABASE_URL = DB_CONFIG['remote_db_url']

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

logger.info('Engine created. Session created')
