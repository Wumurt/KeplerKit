# Парсинг TLE и его запись в текстовый файл в папку с данными

import requests
from bs4 import BeautifulSoup
from src.config import N2YO_API_KEY


def get_tle_from_n2yo(norad_id):
    url = f"https://api.n2yo.com/rest/v1/satellite/tle/{norad_id}&apiKey={N2YO_API_KEY}"

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception('Failed to get data from n2yo.com')

    data = response.json()
    name = data['info']['satname']
    tle = data['tle'].replace('\r\n', '\n')
    return name, tle


def parser(page_url, name_output_file, missing_ids_file=None):
    # 1. Парсим данные с celestrak.org
    r = requests.get(page_url)
    print(f'URL= {page_url} STATUS={r.status_code}')
    html = BeautifulSoup(r.content, 'html.parser')

    # записываем результат в файл
    with open(name_output_file, 'w') as f:
        f.writelines(str(html).split('\n'))

    print(name_output_file, 'from celestrak saved')

    # 2. Добавляем отсутствующие спутники из missing_ids_file для поиска на n2yo
    if missing_ids_file:
        with open(missing_ids_file, 'r') as rfile:
            ids = [line.split()[0] for line in rfile.read().splitlines()]
            print(f'Открыты {ids=} для обработки')
            for n_id in ids:
                name, tle = get_tle_from_n2yo(n_id)
                with open(name_output_file, 'a') as f:
                    f.write(f"{name}\n{tle}\n")
                print(f"[+] Добавлен NORAD {n_id} ({name}) из N2YO в {name_output_file}")
