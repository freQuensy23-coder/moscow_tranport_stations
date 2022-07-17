import pandas as pd

from time import time
from itertools import combinations

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

from config import DB_ECHO, getConnectStr
from cl_arguments import parser

engine = create_engine(getConnectStr(parser.parse_args().loglevel), echo=DB_ECHO,
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


class Cleaner:
    def __init__(self):
        pass

    @staticmethod
    def get_cleaned():
        start = time()
        df = pd.read_sql_table('prediction_data', 'sqlite:///db/test.db', index_col='id')
        df_cleaned = pd.DataFrame(columns=df.columns)

        for stop in df['stop_id'].unique():
            for route in df[df['stop_id'] == stop]['routePathId'].unique():
                for bus in df[(df['stop_id'] == stop) &
                              (df['routePathId'] == route)]['tmId'].unique():
                    rows = df[
                        (df['stop_id'] == stop) &
                        (df['routePathId'] == route) &
                        (df['tmId'] == bus)]

                    pairs = combinations(rows.index, 2)

                    for pair in pairs:
                        if abs(int(df.loc[pair[0], :]['forecast_time']) -
                               int(df.loc[pair[1], :]['forecast_time'])) < 600:
                            if int(df.loc[pair[0], :]['request_time']) < int(df.loc[pair[1], :]['request_time']):
                                pd.concat(df_cleaned, df.loc[pair[0], :])
                            else:
                                pd.concat([df_cleaned, df.loc[pair[1], :]])

        df_cleaned.drop_duplicates(inplace=True)
        print(f'Elapsed: {time() - start} seconds')
        return df_cleaned


Base.metadata.create_all(engine)
