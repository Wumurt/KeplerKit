# Подключение к PostgreSQL (используя SQLAlchemy)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.settings import DB_CONFIG
from src.models import Base
import logging

logger = logging.getLogger(__name__)

# вариант конфигурации БД - облако, если нет - локальный постгрес, если нет - то sqllite
if DB_CONFIG['remote_db_url'] is not None:
    # Строка подключения к удаленному постгресу
    DATABASE_URL = DB_CONFIG['remote_db_url']
    db_type = 'remote'

elif DB_CONFIG['host'] is not None:
    # Строка подключения к локальному постгресу
    DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    db_type = 'host'

else:
    DATABASE_URL = "sqlite:///local.db"
    db_type = "sqlite"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

logger.info("Database engine created, db type: %s", db_type)

if db_type == "sqlite":
    logger.warning("No PostgreSQL config found → using SQLite (development only!)")
    # создаем все таблицы если используется sqlite
    Base.metadata.create_all(bind=engine)
