# Подключение к PostgreSQL (используя SQLAlchemy)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import DB_CONFIG

# Строка подключения к локальному постгресу
# DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"

# Строка подключения к удаленному постгресу
DATABASE_URL = DB_CONFIG['remote_db_url']
# ---
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

print('[INFO] Engine created. Session created')
