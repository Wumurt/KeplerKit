# точка входа

from src.tle_parser import parser
from src.read_tle import read_tle_file
from src.processor import process_tle_records
from src.exporter import export_to_excel
from src.config.settings import OBSERVER, LOG_LEVEL
from src.utils import get_output_dir
import time
import logging
from src.config.logging_config import setup_logging


def main():
    # стартовое время
    time_start = time.perf_counter()

    # инициализация логгера проекта
    setup_logging(LOG_LEVEL)

    # инициализация логгера модуля
    logger = logging.getLogger(__name__)
    logger.info("Application started")

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
    logger.info('Uploading time: %f', time.perf_counter() - time_start)  # 48.72

    # экспорт в Excel последних записей из БД c дельтой между текущим значением и средним за месяц
    export_to_excel(output_file_path=name_output_xlsx_file)

    # итоговое время работы скрипта
    logger.info('Total time: %f', time.perf_counter() - time_start)  # 50.50


if __name__ == '__main__':
    main()
