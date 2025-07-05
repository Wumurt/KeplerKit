# точка входа

# satellite_project/
# ├── data/
# │   └── tle_raw.txt         # Временное хранилище TLE
# ├── db/
# │   └── init.sql            # Скрипт создания таблиц
# ├── src/
# │   ├── config.py           # Настройки подключения к БД
# │   ├── database.py         # Подключение к PostgreSQL
# │   ├── models.py           # SQLAlchemy ORM модели
# │   ├── tle_parser.py       # Парсинг TLE
# │   ├── calculator.py       # Расчет азимута, угла места и пр.
# │   ├── importer.py         # Загрузка TLE в БД
# │   ├── processor.py        # Обработка и расчеты
# │   └── exporter.py         # Экспорт в Excel
# ├── requirements.txt
# └── main.py                 # Точка входа


# tle_parser.py: читает tle_raw.txt, возвращает список TLE-записей с именами спутников
# tle_to_db.py: вставляет новые записи в таблицу satellites
# calculator.py: выполняет расчеты (используя pyorbital, sgp4, skyfield и др.)
# processor.py: получает спутники из БД, производит расчеты, сохраняет результаты в таблицу calculations
# exporter.py: экспортирует расчеты в Excel-файл
# main.py: последовательный запуск всех этапов

# пример основного скрипта
# from src.tle_to_db import import_tle_data
# from src.processor import process_all_satellites
# from src.exporter import export_to_excel
#
# def main():
#     import_tle_data('data/tle_raw.txt')
#     process_all_satellites()
#     export_to_excel('results.xlsx')

from src.tle_parser import parser
from src.read_tle import read_tle_file
from src.processor import process_tle_records


def main():
    # названия выходных файлов и url'ы
    name_output_tle_file = 'data/all_active_satellites.txt'
    url = 'https://celestrak.org/NORAD/elements/geo.txt'

    # парсим и создаем файл с сырыми tle
    parser(url, name_output_tle_file)

    # считываем файл tle в список
    tle_list = read_tle_file(name_output_tle_file)

    # вызываем функцию для обработки данных
    # 'XX.XXXXXX' - долгота (longitude), 'YY.YYYYYY' - широта (latitude)
    process_tle_records(tle_list, observer_lat=YY.YYYYYY, observer_lon=XX.XXXXXX)


if __name__ == '__main__':
    main()
