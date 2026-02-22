# Обработка TLEs, расчеты с помощью модуля src.calculator, запись в базу данных
from src.database import SessionLocal
from src.models import Satellite, Calculation
from src.calculator import calculate_observation
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


def process_tle_records(tle_list, observer_lat, observer_lon):
    with SessionLocal() as session:
        try:
            # 1) Загружаем все спутники одной выборкой
            existing_sats = {sat.norad_id: sat for sat in session.query(Satellite).all()}

            new_satellite_rows = []
            update_satellite_rows = []
            calculation_rows = []

            # --- 2) Обработка TLE ---
            for name, line1, line2 in tle_list:
                result = calculate_observation(name, line1, line2, observer_lat, observer_lon)

                norad = result["norad_id"]
                sat = existing_sats.get(norad)

                # Новый спутник
                if sat is None:
                    new_satellite_rows.append({
                        "name": result["name"],
                        "norad_id": result["norad_id"],
                        "cospar_id": result["cospar_id"],
                        "inclination": result["inclination"],
                        "tle1": result["tle1"],
                        "tle2": result["tle2"],
                        "tle_created_at": result["tle_created_at"],
                    })

                # Существующий спутник — обновляем
                else:
                    update_satellite_rows.append({
                        "id": sat.id,
                        "name": result["name"],
                        "cospar_id": result["cospar_id"],
                        "inclination": result["inclination"],
                        "tle1": result["tle1"],
                        "tle2": result["tle2"],
                        "tle_created_at": result["tle_created_at"],
                    })

                # Записываем расчёт (satellite_id добавим после вставки новых спутников)
                calculation_rows.append({
                    "norad_id": norad,
                    "calculation_time": result["calculation_time"],
                    "latitude": result["latitude"],
                    "longitude": result["longitude"],
                    "altitude": result["altitude"],
                    "azimuth": result["azimuth"],
                    "elevation": result["elevation"],
                    "tle_snapshot": f"{result['tle1']}\n{result['tle2']}",
                })

            # --- 3) Вставка новых спутников ---
            if new_satellite_rows:
                session.bulk_insert_mappings(Satellite, new_satellite_rows)
                session.flush()

                # Получаем вставленные строки c id
                inserted = session.query(Satellite).filter(
                    Satellite.norad_id.in_([row["norad_id"] for row in new_satellite_rows])).all()

                for sat in inserted:
                    existing_sats[sat.norad_id] = sat

            # --- 4) Массовое обновление существующих ---
            if update_satellite_rows:
                session.bulk_update_mappings(Satellite, update_satellite_rows)

            # --- 5) Заполняем satellite_id и готовим данные для вставки ---
            calcs = []
            for row in calculation_rows:
                sat = existing_sats[row["norad_id"]]

                calcs.append({
                    "satellite_id": sat.id,
                    "calculation_time": row["calculation_time"],
                    "latitude": row["latitude"],
                    "longitude": row["longitude"],
                    "altitude": row["altitude"],
                    "azimuth": row["azimuth"],
                    "elevation": row["elevation"],
                    "tle_snapshot": row["tle_snapshot"],
                })

            # --- 6) Массовая вставка расчетов ---
            if calcs:
                session.bulk_insert_mappings(Calculation, calcs)

            session.commit()
            logger.info('Bulk database upload completed')

        except SQLAlchemyError as db_err:
            session.rollback()
            logger.exception("[DB ERROR] %s", db_err)
            raise

        except Exception as e:
            session.rollback()
            logger.exception("[UNEXPECTED ERROR] %s", e)
            raise
