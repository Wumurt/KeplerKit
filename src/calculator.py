# Расчет азимута, угла места и пр. на основе epthem
import ephem
import math
from datetime import datetime, timedelta, timezone


def calculate_observation(name, line1, line2, observer_lat, observer_lon):
    now_utc = datetime.now(timezone.utc)
    tle_obj = ephem.readtle(name, line1, line2)
    tle_obj.compute()

    # географическое положение спутника
    lat = float(tle_obj.sublat) * 180.0 / math.pi
    lon = float(tle_obj.sublong) * 180.0 / math.pi

    # параметры из TLE
    inc = float(line2[8:16])
    norad = int(line2[2:7])
    cospar = line1[9:16]
    epoch_days = float(line1[18:32])
    tle_created_at = datetime(now_utc.year, 1, 1) + timedelta(days=epoch_days)

    # расчет высоты (по орбитальному периоду)
    Gm = 3.986004415e14
    T = 86400 / float(line2.split()[7])
    alt_km = ((Gm * (T / (2 * math.pi)) ** 2) ** (1 / 3) - 6378137) / 1000

    # положение спутника с точки наблюдения
    observer = ephem.Observer()
    observer.lat = str(observer_lat)
    observer.lon = str(observer_lon)
    observer.date = now_utc
    tle_obj.compute(observer)

    az = float(tle_obj.az) * 180.0 / math.pi
    el = float(tle_obj.alt) * 180.0 / math.pi

    return {
        'name': name,
        'norad_id': norad,
        'cospar_id': cospar,
        'inclination': inc,
        'tle1': line1,
        'tle2': line2,
        'tle_created_at': tle_created_at,
        'calculation_time': now_utc,
        'latitude': lat,
        'longitude': lon,
        'altitude': alt_km,
        'azimuth': az,
        'elevation': el,
    }
print(f'{__name__} completed')
