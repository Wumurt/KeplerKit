import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем из .env

DB_CONFIG = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'dbname': os.getenv('DB_NAME'),
}

N2YO_API_KEY = os.getenv('N2YO_API_KEY')

print(f'[INFO] Config successfully loaded!')
