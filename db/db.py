from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import create_engine

import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from config import DB_CONNECTION_STRING, DB_ECHO


engine = create_engine(DB_CONNECTION_STRING, echo=DB_ECHO,
                       pool_size=10,
                       max_overflow=2,
                       pool_recycle=300,
                       pool_pre_ping=True,
                       pool_use_lifo=True)
Base = declarative_base()


class Prediction(Base):
    __tablename__ = "prediction_data"
    id = Column(Integer, primary_key=True)
    stop_id = Column(String)
    route_path_id = Column(String)
    forecast_time = Column(Integer)
    byTelemetry = Column(Integer)
    tmId = Column(Integer)
    routePathId = Column(String)
    request_time = Column(Integer)


class Stop(Base):
    __tablename__ = 'stops'
    id = Column(Integer, primary_key=True)
    stop_id = Column(String)
    name = Column(String)

    route_path_id = Column(String)
    routePathId = Column(String)
    transport_type = Column(String)
    number = Column(String)
    last_stop_name = Column(String)

    lon = Column(Float)
    lat = Column(Float)


Base.metadata.create_all(engine)
