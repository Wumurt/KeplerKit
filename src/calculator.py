# Расчет азимута, угла места и пр. на основе epthem
from datetime import datetime, timedelta, timezone
import ephem
import math
import logging

logger = logging.getLogger(__name__)


def parse_tle_epoch(epoch_str):
    year = int(epoch_str[:2])
    if year < 57:
        year += 2000
    else:
        year += 1900

    day_of_year = float(epoch_str[2:])
    day_int = int(day_of_year)
    day_frac = day_of_year - day_int

    base_date = datetime(year, 1, 1, tzinfo=timezone.utc) + timedelta(days=day_int - 1)
    seconds_in_day = 86400
    time_part = timedelta(seconds=day_frac * seconds_in_day)

    return base_date + time_part


def calculate_observation(name, line1, line2, observer_lat, observer_lon):
    now_utc = datetime.now(timezone.utc)
    tle_obj = ephem.readtle(name, line1, line2)

    # субспутниковая точка
    tle_obj.compute(now_utc)
    lat = float(tle_obj.sublat) * 180.0 / math.pi
    lon = float(tle_obj.sublong) * 180.0 / math.pi

    # inclination
    inc = float(line2.split()[2])

    # NORAD
    norad = int(line2[2:7])
    cospar = line1[9:16]

    # корректное определение эпохи TLE
    year = int(line1[18:20])
    if year < 57:
        year += 2000
    else:
        year += 1900
    epoch_str = line1[18:32]
    tle_created_at = parse_tle_epoch(epoch_str)

    # высота по периоду
    Gm = 3.986004415e14
    T = 86400 / float(line2.split()[7])
    alt_km = ((Gm * (T / (2 * math.pi)) ** 2) ** (1 / 3) - 6378137) / 1000

    # расчет азимута и угла места
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


# запись о загрузке модуля
logger.debug('%s loaded', __name__)
