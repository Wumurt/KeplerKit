# Экспорт в Excel / Экспорт в Excel с дельтами

import pandas as pd
from sqlalchemy import select, func
from src.database import SessionLocal
from src.models import Satellite, Calculation
from datetime import timedelta


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
    df.to_excel(output_file_path, sheet_name='Sats', index=False)
    print(f'Данные экспортированы в {output_file_path}')


def find_nearest_calculation(session, satellite_id, target_time):
    return session.query(Calculation) \
        .filter(Calculation.satellite_id == satellite_id) \
        .order_by(func.abs(func.extract('epoch', Calculation.calculation_time - target_time))) \
        .first()


def export_to_excel_with_deltas(output_file_path: str, _debug_count=0):
    session = SessionLocal()
    data = []

    satellites = session.query(Satellite).all()

    for sat in satellites:
        latest = session.query(Calculation) \
            .filter_by(satellite_id=sat.id) \
            .order_by(Calculation.calculation_time.desc()) \
            .first()

        if not latest:
            continue

        now = latest.calculation_time
        targets = {
            '1d': now - timedelta(days=1),
            '7d': now - timedelta(days=7),
            '30d': now - timedelta(days=30),
        }

        nearest = {k: find_nearest_calculation(session, sat.id, t) for k, t in targets.items()}

        def delta_lon(old):
            return latest.longitude - old.longitude if old else None

        # check first 10 rows in the console
        if _debug_count < 10:
            print(f"[{sat.name}] Последняя дата: {now}")
            for key, record in nearest.items():
                if record:
                    delta = abs((record.calculation_time - targets[key]).total_seconds()) / 3600
                    print(f"  {key}: ближайшая запись — {record.calculation_time} (разница ~{delta:.1f} ч)")
                else:
                    print(f"  {key}: запись не найдена")
            _debug_count += 1

        # continue script
        data.append({
            'ИСЗ': sat.name,
            'Долгота': latest.longitude,
            'Широта': latest.latitude,
            'Азимут': latest.azimuth,
            'Угол места': latest.elevation,
            '№ NORAD': sat.norad_id,
            'Межд.номер': sat.cospar_id,
            'Наклонение': sat.inclination,
            'Высота': latest.altitude,
            'Дата создания TLE': sat.tle_created_at,
            'Дата расчетов': latest.calculation_time,
            'Δ долготы за 1 день': delta_lon(nearest['1d']),
            'Δ долготы за 7 дней': delta_lon(nearest['7d']),
            'Δ долготы за 30 дней': delta_lon(nearest['30d']),
        })

    output_file_path = f'{output_file_path.split('.')[0]}_deltas.xlsx'

    df = pd.DataFrame(data)
    df.sort_values(by='Долгота', inplace=True)
    df.to_excel(output_file_path, sheet_name='Sats_delta', index=False)
    print(f'Данные с дельтами экспортированы в {output_file_path}')

    session.close()


if __name__ == '__main__':
    export_to_excel('exported_satellites.xlsx')
