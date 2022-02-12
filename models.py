from time import time

import sqlalchemy.orm
from pydantic import BaseModel, Field
from db.db import Prediction
import db.db


class Forecast(BaseModel):
    time: int
    byTelemetry: int
    tmId: int
    routePathId: str


class RotePath(BaseModel):
    id_: str = Field(alias="id")
    transport_type: str = Field(alias="type")
    number: str
    lastStopName: str
    externalForecast: list[Forecast]


class Stop(BaseModel):
    id_: str = Field(alias="id")
    name: str
    route_path: list[RotePath] = Field(alias="routePath")
    lon: float
    lat: float

    def save_forecast(self, session: sqlalchemy.orm.Session, req_time: int = int(time()), commit=False):
        for path in self.route_path:
            for forecast in path.externalForecast:
                p = Prediction(
                    stop_id=self.id_,
                    route_path_id=path.id_,
                    forecast_time=forecast.time + req_time,
                    byTelemetry=forecast.byTelemetry,
                    tmId=forecast.tmId,
                    routePathId=forecast.routePathId,
                    request_time=req_time
                )
                session.add(p)
        if commit:
            session.commit()

    def save_stop(self, session: sqlalchemy.orm.Session, commit=False):
        for r in self.route_path:
            if len(r.externalForecast) != 0:
                s = db.db.Stop(
                    stop_id=self.id_,
                    name=self.name,
                    route_path_id=r.id_,
                    routePathId=r.externalForecast[0].routePathId,
                    transport_type=r.transport_type,
                    number=r.number,
                    last_stop_name=r.lastStopName,
                    lat=self.lat,
                    lon=self.lon
                )
                session.add(s)
        if commit:
            session.commit()
