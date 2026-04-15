🛰 KeplerKit

KeplerKit — это Python-пайплайн для загрузки, обработки и анализа TLE-данных геостационарных спутников с последующим сохранением в базу данных и экспортом в Excel.

Проект автоматически:

загружает актуальные TLE
дополняет недостающие спутники через API
рассчитывает параметры наблюдения
сохраняет результаты в БД
экспортирует отчёт в .xlsx
📦 Возможности
📡 Загрузка TLE с CelesTrak
🔍 Дозагрузка спутников через N2YO API
🧮 Расчёт:
субспутниковой точки
азимута и угла места
высоты орбиты
🗄️ Поддержка:
PostgreSQL
SQLite (fallback)
📊 Экспорт в Excel
📝 Логирование с ротацией
🏗️ Структура проекта
KeplerKit/
│
├── main.py                # Точка входа
├── requirements.txt
├── .env.example
│
├── db/
│   └── init.sql          # SQL-схема
│
├── src/
│   ├── calculator.py     # Расчёты
│   ├── database.py       # Подключение к БД
│   ├── exporter.py       # Экспорт в Excel
│   ├── models.py         # ORM модели
│   ├── processor.py      # Обработка данных
│   ├── read_tle.py       # Чтение TLE
│   ├── tle_parser.py     # Загрузка и парсинг TLE
│   ├── utils.py
│   │
│   └── config/
│       ├── settings.py
│       └── logging_config.py
│
└── data/
    ├── logs/
    └── YYYY/MM/DD/
⚙️ Установка
git clone https://github.com/Wumurt/KeplerKit.git
cd KeplerKit

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
🔑 Настройка

Создай .env на основе примера:

cp .env.example .env

Заполни:

GEO_URL=https://celestrak.org/NORAD/elements/gp.php?GROUP=geo&FORMAT=tle

# Координаты наблюдателя
OBSERVER_LAT=55.75
OBSERVER_LON=37.62

# База данных
DB_HOST=localhost
DB_PORT=5432
DB_NAME=kepler
DB_USER=postgres
DB_PASSWORD=password

# API
N2YO_API_KEY=your_api_key

# Логирование
LOG_LEVEL=INFO
🗄️ База данных
PostgreSQL (рекомендуется)

Создай БД и применяй схему:

psql -U postgres -d kepler -f db/init.sql
SQLite (fallback)

Если PostgreSQL недоступен — база создастся автоматически.

▶️ Запуск
python main.py
📊 Результаты

После запуска:

📁 TLE файл:

data/YYYY/MM/DD/active_geo_satellites.txt

📊 Excel отчёт:

data/YYYY/MM/DD/active_geo_satellites.xlsx

📝 Логи:

data/logs/app.log
🔄 Pipeline
Загрузка TLE
Дозагрузка недостающих спутников (N2YO)
Парсинг TLE
Расчёт параметров
Сохранение в БД
Экспорт в Excel
⚠️ Ограничения
Нет миграций БД (используется init.sql)
Ограниченная валидация входных данных
Возможна утечка API-ключа в debug-логах
Зависимость от внешних API (CelesTrak, N2YO)
🚧 TODO
 Добавить Alembic (миграции)
 Улучшить обработку ошибок
 Покрыть тестами
 CLI-интерфейс
 Docker
 Кэширование API-запросов
📜 Лицензия

MIT License (или укажи свою)

👨‍💻 Автор

Wumurt
