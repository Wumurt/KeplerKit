# точка входа

import sys
from pathlib import Path
from time import perf_counter
from src.tle_parser import parser
from src.read_tle import read_tle_file
from src.processor import process_tle_records
from src.exporter import export_to_excel
from src.config.settings import OBSERVER, LOG_LEVEL, GEO_URL
from src.utils import get_output_dir
import logging
from src.config.logging_config import setup_logging

# инициализация логгера на уровне модуля
logger = logging.getLogger(__name__)


def run_pipeline(
        url: str,
        output_dir: Path,
        observer_lat: float,
        observer_lon: float,
        out_filename: str = 'active_geo_satellites',
        missing_ids_file: str | Path = Path('data/missing_norad_ids.txt')

) -> None:
    """Загружает TLE по URL, обрабатывает, заносит данные в БД и экспортирует результаты в Excel."""

    logger.info('Pipeline started')

    # названия выходных файлов
    base_name = output_dir / out_filename
    name_output_tle_file = base_name.with_suffix('.txt')
    name_output_xlsx_file = base_name.with_suffix('.xlsx')
    logger.debug('base_name: %s, tle: %s, xlsx: %s', base_name, name_output_tle_file, name_output_xlsx_file)

    # парсим и создаем текстовый файл с необработанными tle
    t0 = perf_counter()
    parser(url, name_output_tle_file, missing_ids_file=missing_ids_file)
    logger.info("Downloaded and parsed TLE in %fs", perf_counter() - t0)

    # считываем файл tle в список
    tle_list = read_tle_file(name_output_tle_file)

    # обновляем данные в таблице БД Satellite, обрабатываем данные, записываем расчеты в Calculations
    t0 = perf_counter()
    process_tle_records(tle_list, observer_lat, observer_lon)
    logger.info("Processed and stored records in %fs", perf_counter() - t0)

    # экспорт в Excel последних записей из БД с отклонением от среднемесячного значения долготы ПСТ
    t0 = perf_counter()
    export_to_excel(output_file_path=name_output_xlsx_file)
    logger.info("Exported to Excel in %fs", perf_counter() - t0)


def main():
    # стартовое время
    time_start = perf_counter()

    # конфигурация логирования проекта
    setup_logging(LOG_LEVEL)
    logger.info('Application started')

    # создаем директорию с сегодняшней датой в формате data/YYYY/MM/DD
    output_dir = get_output_dir(base_dir='data', nested=True)

    try:
        # запускаем пайплайн
        run_pipeline(GEO_URL,
                     output_dir,
                     OBSERVER['observer_lat'],
                     OBSERVER['observer_lon'],
                     out_filename='active_geo_satellites')

        logger.info("Pipeline finished successfully! Total time: %fs", perf_counter() - time_start)
        # возврат exit code операционной системе
        return 0

    except Exception:
        logger.exception('Pipeline failed at %fs', perf_counter() - time_start)
        return 1


if __name__ == '__main__':
    sys.exit(main())
