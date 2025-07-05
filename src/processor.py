# Обработка TLEs, расчеты с помощью модуля src.calculator, запись в базу данных

from src.database import SessionLocal
from src.models import Satellite, Calculation
from src.calculator import calculate_observation


def process_tle_records(tle_list, observer_lat, observer_lon):
    session = SessionLocal()

    for name, line1, line2 in tle_list:
        result = calculate_observation(name, line1, line2, observer_lat, observer_lon)

        # найти или создать спутник по NORAD ID
        sat = session.query(Satellite).filter_by(norad_id=result['norad_id']).first()

        if not sat:
            sat = Satellite(
                name=result['name'],
                norad_id=result['norad_id'],
                cospar_id=result['cospar_id'],
                inclination=result['inclination'],
                tle1=result['tle1'],
                tle2=result['tle2'],
                tle_created_at=result['tle_created_at']
            )
            session.add(sat)
            session.flush()  # получить ID нового спутника
        else:
            # обновить TLE
            sat.tle1 = result['tle1']
            sat.tle2 = result['tle2']
            sat.tle_created_at = result['tle_created_at']
            sat.inclination = result['inclination']
            sat.name = result['name']
            sat.cospar_id = result['cospar_id']
            session.flush()

        # записать результат расчета
        calc = Calculation(
            satellite_id=sat.id,
            calculation_time=result['calculation_time'],
            latitude=result['latitude'],
            longitude=result['longitude'],
            altitude=result['altitude'],
            azimuth=result['azimuth'],
            elevation=result['elevation']
        )
        session.add(calc)

    session.commit()
    print(f'Load to DB done')
    session.close()
    print('session closed')
print(f'{__name__} done')
