from sqlalchemy import Column, Integer, Text, Float, Double, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import logging

logger = logging.getLogger(__name__)
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
    # добавляем связь между таблицами в алхимии
    calculations = relationship("Calculation", back_populates="satellite", cascade="all, delete")


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
    tle_snapshot = Column(Text, nullable=True)  # TLE, использованный при расчёте (tle1 + "\n" + tle2)
    # добавляем связь между таблицами в алхимии
    satellite = relationship("Satellite", back_populates="calculations")


logger.info('Models created. %s completed', __name__)
