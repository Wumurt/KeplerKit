from sqlalchemy import Column, Integer, Text, Float, Double, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Satellite(Base):
    __tablename__ = 'satellites'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    norad_id = Column(Integer, unique=True, nullable=False)
    cospar_id = Column(Text)
    inclination = Column(Float)
    tle1 = Column(Text, nullable=False)
    tle2 = Column(Text, nullable=False)
    tle_created_at = Column(TIMESTAMP, nullable=False)


class Calculation(Base):
    __tablename__ = 'calculations'

    id = Column(Integer, primary_key=True)
    satellite_id = Column(Integer, ForeignKey('satellites.id', ondelete="CASCADE"))
    latitude = Column(Double)
    longitude = Column(Double)
    altitude = Column(Double)
    azimuth = Column(Double)
    elevation = Column(Double)
    calculation_time = Column(TIMESTAMP, nullable=False)

print(f'{__name__} completed')
