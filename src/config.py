# Настройки подключения к БД
DB_CONFIG = {
    'user': 'postgres',
    'password': '1234',
    'host': 'localhost',
    'port': '5432',
    'dbname': 'mydb'
}

N2YO_API_KEY ='"111111-222222-333333-4444"'

# переделать под переменные среды

# 🔒 Рекомендации по безопасности
# Чтобы не хранить пароли в открытом виде:
#
# Используй .env файл и библиотеку python-dotenv.
#
# Обнови config.py для чтения переменных среды:
#
# ✅ .env (в корне проекта)
# env
#
# DB_USER=your_db_user
# DB_PASSWORD=your_db_password
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=your_database_name
# ✅ src/config.py с dotenv
#
# import os
# from dotenv import load_dotenv
#
# load_dotenv()  # Загружаем из .env
#
# DB_CONFIG = {
#     'user': os.getenv('DB_USER'),
#     'password': os.getenv('DB_PASSWORD'),
#     'host': os.getenv('DB_HOST'),
#     'port': os.getenv('DB_PORT'),
#     'dbname': os.getenv('DB_NAME'),
# }
# И не забудь установить зависимость:
#
# pip install python-dotenv