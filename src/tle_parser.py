# Парсинг TLE и его запись в текстовый файл в папку с данными

import requests
from bs4 import BeautifulSoup


def parser(page_url, name_output_file):
    # парсим данные
    r = requests.get(page_url)
    print(f'URL= {page_url} STATUS={r.status_code}')
    html = BeautifulSoup(r.content, 'html.parser')

    # записываем результат в файл
    with open(name_output_file, 'w') as f:
        f.writelines(str(html).split('\n'))

    print(name_output_file, 'saved')
