# точка входа

from src.tle_parser import parser
from src.read_tle import read_tle_file
from src.processor import process_tle_records
from src.exporter import export_to_excel
from src.config import OBSERVER
from src.utils import get_output_dir
import time


def main():
    # стартовое время
    time_start = time.time()

    # названия выходных файлов и url'ы
    url = 'https://celestrak.org/NORAD/elements/geo.txt'

    output_dir = get_output_dir(base_dir='data', nested=True)
    base_name = output_dir / 'active_geo_satellites'
    name_output_tle_file = f"{base_name}.txt"
    name_output_xlsx_file = f"{base_name}.xlsx"

    # парсим и создаем файл с сырыми tle
    parser(url, name_output_tle_file, missing_ids_file='data/missing_norad_ids.txt')

    # считываем файл tle в список
    tle_list = read_tle_file(name_output_tle_file)

    # вызываем функцию для обработки данных
    process_tle_records(tle_list, OBSERVER['observer_lat'], OBSERVER['observer_lon'])

    # время на запись в БД
    print(f'[INFO] Uploading time: {time.time()-time_start}') # 48.72

    # экспорт в Excel последних записей из БД c дельтой между текущим значением и средним за месяц
    export_to_excel(output_file_path=name_output_xlsx_file)

    # итоговое время работы скрипта
    print(f'[INFO] Total time: {time.time() - time_start}') # 50.50
if __name__ == '__main__':
    main()
