# Экспорт в Excel

import pandas as pd
from sqlalchemy import select
from src.database import SessionLocal
from src.models import Satellite, Calculation


def export_to_excel(output_file_path: str):
    session = SessionLocal()

    # Словарь для хранения самых свежих расчётов по каждому спутнику
    latest_calculations = {}

    # Получаем все расчёты, отсортированные по времени
    results = session.execute(
        select(Calculation).order_by(Calculation.calculation_time.desc())
    ).scalars().all()

    for calc in results:
        sat = calc.satellite
        if sat.norad_id not in latest_calculations:
            latest_calculations[sat.norad_id] = {
                'ИСЗ': sat.name,
                'Долгота': calc.longitude,
                'Широта': calc.latitude,
                'Азимут': calc.azimuth,
                'Угол места': calc.elevation,
                '№ NORAD': sat.norad_id,
                'Межд.номер': sat.cospar_id,
                'Наклонение': sat.inclination,
                'Высота': calc.altitude,
                'Дата создания TLE': sat.tle_created_at,
                'Дата расчетов': calc.calculation_time,
            }

    session.close()

    # Преобразуем в DataFrame и сортируем по долготе
    df = pd.DataFrame(latest_calculations.values())
    df.sort_values(by='Долгота', inplace=True)

    # Экспорт в Excel
    df.to_excel(output_file_path, sheet_name='Спутники', index=False)
    print(f'Данные экспортированы в {output_file_path}')


if __name__ == '__main__':
    export_to_excel('exported_satellites.xlsx')
