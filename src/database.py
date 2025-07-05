# Подключение к PostgreSQL (используя SQLAlchemy)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import DB_CONFIG

DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
