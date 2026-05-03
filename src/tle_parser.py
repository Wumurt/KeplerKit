# Парсинг TLE и его запись в текстовый файл в папку с данными

import requests
from bs4 import BeautifulSoup
from src.config.settings import N2YO_API_KEY
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def get_tle_from_n2yo(norad_id: str) -> tuple[str, str]:
    url = f"https://api.n2yo.com/rest/v1/satellite/tle/{norad_id}&apiKey={N2YO_API_KEY}"
    response = requests.get(url, timeout=5)
    logger.debug('response.url: %s, response.text: %s', response.url, response.text)
    if response.status_code != 200:
        logger.error('response.status_code=%s', response.status_code)
        raise Exception(f'Не удалось получить TLE с N2YO для {norad_id}, {response.status_code=}')

    data = response.json()
    name = data['info']['satname']
    tle = data['tle'].replace('\r\n', '\n')  # нормализуем перевод строки
    return name, tle


def extract_norad_ids_from_tle(lines: list[str]) -> set[int]:
    ids = set()
    for line in lines:
        if line.startswith("2 "):  # строка 2 в TLE
            try:
                norad_id = int(line[2:7])
                ids.add(norad_id)
            except ValueError:
                logger.exception("ValueError")
                continue
    return ids


def parser(page_url: str, name_output_file: str | Path, missing_ids_file: str | None = None):
    logger.info('Загружаем TLE с %s', page_url)
    r = requests.get(page_url)
    logger.debug('Ответ Celestrak: STATUS=%d', r.status_code)
    html = BeautifulSoup(r.content, 'html.parser')

    # 1. Сохраняем TLE из Celestrak
    tle_lines = str(html).split('\n')
    with open(name_output_file, 'w') as f:
        f.writelines(tle_lines)

    logger.info('%d TLE с Celestrak сохранены в %s', len(tle_lines) // 3, name_output_file)

    # 2. Загружаем NORAD ID из уже записанных TLE
    existing_ids = extract_norad_ids_from_tle(tle_lines)
    logger.debug('Извлечено %d NORAD ID из Celestrak', len(existing_ids))

    # 3. Если есть список пропущенных — проверяем и дополняем
    try:
        if missing_ids_file:
            with open(missing_ids_file, 'r') as rfile:
                missing_ids = [line.split()[0] for line in rfile.read().strip().splitlines()]
                logger.debug('Считано id_norad %d, missing_ids: %s', len(missing_ids), missing_ids)

            missing_tles = []  # собираем в память строки для дозаписи
            for norad_id in missing_ids:
                if int(norad_id) in existing_ids:
                    logger.info('[SKIP] NORAD %s уже есть в файле %s — пропускаем', norad_id, name_output_file)
                    continue
                try:
                    name, tle = get_tle_from_n2yo(norad_id)
                    missing_tles.append(f"{name}\n{tle}\n")
                    logger.info('[+] Добавлен NORAD %s — %s с N2YO', norad_id, name)
                except Exception as e:
                    logger.exception('NORAD %s — ошибка при получении с N2YO: %s', norad_id, e)
            # дозаписываем собранные данные
            if missing_tles:
                with open(name_output_file, 'a') as f:
                    f.writelines(missing_tles)
                logger.info('Записано %d ИСЗ с N2YO в %s', len(missing_tles), name_output_file)
    except FileNotFoundError as e:
        logger.critical('Файл %s не найден', missing_ids_file)
