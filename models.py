from time import time

import sqlalchemy.orm
from pydantic import BaseModel, Field
from db.db import Prediction


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

    def save(self, session: sqlalchemy.orm.Session, req_time: int = int(time()), commit=False):
        for path in self.route_path:
            for forecast in path.externalForecast:
                p = Prediction(
                    stop_id=self.id_,
                    stop_name=self.name,
                    route_path_id=path.id_,
                    transport_type=path.transport_type,
                    number=path.number,
                    lastStopName=path.lastStopName,
                    forecast_time=forecast.time + req_time,
                    byTelemetry=forecast.byTelemetry,
                    tmId=forecast.tmId,
                    routePathId=forecast.routePathId,
                    request_time=req_time
                )
                session.add(p)
        if commit:
            session.commit()
