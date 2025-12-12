# точка входа

from src.tle_parser import parser
from src.read_tle import read_tle_file
from src.processor import process_tle_records
from src.exporter import export_to_excel, export_to_excel_with_deltas
from src.config import OBSERVER
import time


def main():
    # стартовое время
    time_start = time.time()

    # названия выходных файлов и url'ы
    name_output_file = 'data/active_geo_satellites'
    name_output_tle_file = name_output_file + '.txt'
    url = 'https://celestrak.org/NORAD/elements/geo.txt'

    # парсим и создаем файл с сырыми tle
    parser(url, name_output_tle_file, missing_ids_file='data/missing_norad_ids.txt')

    # считываем файл tle в список
    tle_list = read_tle_file(name_output_tle_file)

    # вызываем функцию для обработки данных
    process_tle_records(tle_list, OBSERVER['observer_lat'], OBSERVER['observer_lon'])

    # время на запись в БД
    print(f'[INFO] Uploading time: {time.time()-time_start}') # NEON 146.9 sec / local 14.91

    # экспорт в Excel последних записей из БД
    name_output_xlsx_file = name_output_file + '.xlsx'
    export_to_excel(output_file_path=name_output_xlsx_file)

    # экспорт в Excel последних записей из БД с дельтой
    export_to_excel_with_deltas(name_output_xlsx_file)

    # итоговое время работы скрипта
    print(f'[INFO] Total time: {time.time() - time_start}') # NEON 387.96 sec / local 34.18
if __name__ == '__main__':
    main()
