from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine

engine = create_engine('sqlite:///db/forecast.db', echo=True)
Base = declarative_base()


class Prediction(Base):
    __tablename__ = "forecast"
    id = Column(Integer, primary_key=True)
    stop_id = Column(Integer)
    stop_name = Column(String)
    route_path_id = Column(Integer)
    transport_type = Column(String)
    number = Column(String)
    lastStopName = Column(String)
    forecast_time = Column(Integer)
    byTelemetry = Column(Integer)
    tmId = Column(Integer)
    routePathId = Column(String)
    request_time = Column(Integer)


Base.metadata.create_all(engine)
