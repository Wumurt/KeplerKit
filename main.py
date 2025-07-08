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

# calculator.py: выполняет расчеты (используя pyorbital, sgp4, skyfield и др.)
# processor.py: получает спутники из БД, производит расчеты, сохраняет результаты в таблицу calculations
# exporter.py: экспортирует расчеты в Excel-файл
# main.py: последовательный запуск всех этапов


from src.tle_parser import parser
from src.read_tle import read_tle_file
from src.processor import process_tle_records
from src.exporter import export_to_excel, export_to_excel_with_deltas


def main():
    # названия выходных файлов и url'ы
    name_output_file = 'data/active_geo_satellites'
    name_output_tle_file = name_output_file + '.txt'
    url = 'https://celestrak.org/NORAD/elements/geo.txt'

    # парсим и создаем файл с сырыми tle
    parser(url, name_output_tle_file, missing_ids_file='data/missing_norad_ids.txt')

    # считываем файл tle в список
    tle_list = read_tle_file(name_output_tle_file)

    # вызываем функцию для обработки данных
    # 'XX.XXXXXX' - долгота (longitude), 'YY.YYYYYY' - широта (latitude)
    process_tle_records(tle_list, observer_lat=YY.YYYYYY, observer_lon=XX.XXXXXX)

    # экспорт в Excel последних записей из БД
    name_output_xlsx_file = name_output_file + '.xlsx'
    export_to_excel(output_file_path=name_output_xlsx_file)

    # экспорт в Excel последних записей из БД с дельтой
    export_to_excel_with_deltas(name_output_xlsx_file)

if __name__ == '__main__':
    main()
