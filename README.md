# 🛰 KeplerKit

**KeplerKit** --- это Python-пайплайн для загрузки, обработки и анализа
TLE-данных геостационарных спутников с последующим сохранением в базу
данных и экспортом в Excel.

## 📦 Возможности

-   📡 Загрузка TLE с CelesTrak
-   🔍 Дозагрузка спутников через N2YO API
-   🧮 Расчёт параметров орбитального положения ИСЗ, азимута и угла места относительно наблюдателя
-   🗄️ Поддержка PostgreSQL и SQLite
-   📊 Экспорт в Excel
-   📝 Логирование с ротацией

## ⚙️ Установка

``` bash
git clone https://github.com/Wumurt/KeplerKit.git
cd KeplerKit

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🔑 Настройка

Создай `.env`:

``` env
GEO_URL=https://celestrak.org/NORAD/elements/gp.php?GROUP=geo&FORMAT=tle
OBSERVER_LAT=55.75
OBSERVER_LON=37.62
DB_HOST=localhost
DB_PORT=5432
DB_NAME=kepler
DB_USER=postgres
DB_PASSWORD=password
N2YO_API_KEY=your_api_key
LOG_LEVEL=INFO
```

## ▶️ Запуск

``` bash
python main.py
```

## 📊 Результаты

-   TLE: `data/YYYY/MM/DD/active_geo_satellites.txt`
-   Excel: `data/YYYY/MM/DD/active_geo_satellites.xlsx`
-   Логи: `data/logs/app.log`

## 📜 Лицензия

MIT
