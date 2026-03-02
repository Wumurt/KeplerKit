# Экспорт в Excel с дельтой текущей долготы и AVG(lat) за последние 30 суток

import time
import pandas as pd
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from src.database import SessionLocal
from src.models import Calculation
from datetime import timedelta
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def export_to_excel(output_file_path: str | Path):
    with SessionLocal() as session:
        # 1) последние расчёты по каждому ИСЗ
        latest_subq = (
            select(
                Calculation.satellite_id,
                func.max(Calculation.calculation_time).label("max_time")
            )
            .group_by(Calculation.satellite_id)
            .subquery()
        )

        latest_calcs = (
            session.query(Calculation)
            .join(
                latest_subq,
                (Calculation.satellite_id == latest_subq.c.satellite_id) &
                (Calculation.calculation_time == latest_subq.c.max_time)
            )
            .options(selectinload(Calculation.satellite))
            .all()
        )

        # 2) средняя долгота за последние 30 суток для всех ИСЗ
        month_avg = (
            session.query(
                Calculation.satellite_id,
                func.avg(Calculation.longitude).label("avg_longitude")
            )
            .filter(
                Calculation.calculation_time >=
                func.now() - timedelta(days=30)
            )
            .group_by(Calculation.satellite_id)
            .all()
        )

        avg_by_sat = {
            row.satellite_id: row.avg_longitude
            for row in month_avg
        }

        # 3) формирование строк для Excel
        rows = []

        for latest in latest_calcs:
            sat = latest.satellite
            avg_lon = avg_by_sat.get(latest.satellite_id)

            delta_from_avg = (
                latest.longitude - avg_lon
                if avg_lon is not None
                else None
            )

            rows.append({
                "ИСЗ": sat.name,
                "Долгота": latest.longitude,
                "Широта": latest.latitude,
                "Азимут": latest.azimuth,
                "Угол места": latest.elevation,
                "№ NORAD": sat.norad_id,
                "Межд.номер": sat.cospar_id,
                "Наклонение": sat.inclination,
                "Высота": latest.altitude,
                "Дата создания TLE (UTC+3)": sat.tle_created_at + timedelta(hours=3),
                "Дата расчетов (UTC+3)": latest.calculation_time + timedelta(hours=3),
                "Средняя долгота за 30 суток": avg_lon,
                "Отклонение от среднемесячной долготы": delta_from_avg,
            })

        df = pd.DataFrame(rows).sort_values("Долгота")
        df.to_excel(output_file_path, index=False)
        logger.info('EXEL FILE: %s created', output_file_path)


logger.info('Exporter successfully loaded')

if __name__ == "__main__":
    time_start = time.time()
    export_to_excel("satellites_test.xlsx")
    print(f'Time execution: {time.time() - time_start}')
