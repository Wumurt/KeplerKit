-- добавить таблицу tles только при необходимости отслеживания TLE как объектов

CREATE TABLE satellites (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    norad_id INTEGER UNIQUE NOT NULL,
    cospar_id TEXT,
    inclination REAL,
    tle1 TEXT NOT NULL,
    tle2 TEXT NOT NULL,
    tle_created_at TIMESTAMP NOT NULL
);

CREATE TABLE calculations (
    id SERIAL PRIMARY KEY,
    satellite_id INTEGER REFERENCES satellites(id) ON DELETE CASCADE,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    altitude DOUBLE PRECISION,
    azimuth DOUBLE PRECISION,
    elevation DOUBLE PRECISION,
    calculation_time TIMESTAMP NOT NULL,
    tle_snapshot TEXT
);
