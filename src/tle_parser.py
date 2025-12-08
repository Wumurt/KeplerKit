# Парсинг TLE и его запись в текстовый файл в папку с данными

import requests
from bs4 import BeautifulSoup
from src.config import N2YO_API_KEY


def get_tle_from_n2yo(norad_id: str) -> tuple[str, str]:
    url = f"https://api.n2yo.com/rest/v1/satellite/tle/{norad_id}&apiKey={N2YO_API_KEY}"
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        print(f'{response.status_code=}')
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
                continue
    return ids


def parser(page_url: str, name_output_file: str, missing_ids_file: str | None = None):
    print(f"[INFO] Загружаем TLE с {page_url}")
    r = requests.get(page_url)
    print(f'[DEBUG] Ответ Celestrak: STATUS={r.status_code}')
    html = BeautifulSoup(r.content, 'html.parser')

    # 1. Сохраняем TLE из Celestrak
    tle_lines = str(html).split('\n')
    with open(name_output_file, 'w') as f:
        f.writelines(tle_lines)

    print(f'[INFO] {len(tle_lines) // 3} TLE с Celestrak сохранены в {name_output_file}')

    # 2. Загружаем NORAD ID из уже записанных TLE
    existing_ids = extract_norad_ids_from_tle(tle_lines)
    print(f"[DEBUG] Извлечено {len(existing_ids)} NORAD ID из Celestrak")

    # 3. Если есть список пропущенных — проверяем и дополняем
    if missing_ids_file:
        with open(missing_ids_file, 'r') as rfile:
            missing_ids = [line.split()[0] for line in rfile.read().strip().splitlines()]
            print(f'[DEBUG] Считано id_norad {len(missing_ids)} {missing_ids=}')

        missing_tles = []  # собираем в память строки для дозаписи
        for norad_id in missing_ids:
            if int(norad_id) in existing_ids:
                print(f"[SKIP] NORAD {norad_id} уже есть в файле {name_output_file} — пропускаем")
                continue
            try:
                name, tle = get_tle_from_n2yo(norad_id)
                missing_tles.append(f"{name}\n{tle}\n")
                print(f"[+] Добавлен NORAD {norad_id} ({name}) с N2YO")
            except Exception as e:
                print(f"[ERROR] NORAD {norad_id} — ошибка при получении с N2YO: {e}")
        # дозаписываем собранные данные
        if missing_tles:
            with open(name_output_file, 'a') as f:
                f.writelines(missing_tles)
            print(f"[INFO] Записано {len(missing_tles)} ИСЗ с N2YO в {name_output_file}")
