import numpy as np
import pandas as pd

from time import time, asctime

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
    def get_csv(file='db.csv'):
        print('Fetching DB...')
        df = pd.read_sql_table('prediction_data', getConnectStr(parser.parse_args().loglevel), index_col='id')
        print('DB fetched')
        df.to_csv(file)

    @staticmethod
    def get_cleaned(read_from=None, write_to=None):
        if read_from is not None:
            df = pd.read_csv(read_from, header=0)
        else:
            print('Fetching DB...')
            df = pd.read_sql_table('prediction_data', getConnectStr(parser.parse_args().loglevel))
            print('DB fetched')
            if write_to is not None:
                df.to_csv(write_to, index=False)

        start = time()
        print(f'\nCleaner started at: {asctime()}')

        data_cleaned = np.array(df.columns)
        i = 0

        for stop in df['stop_id'].unique():
            for route in df[df['stop_id'] == stop]['routePathId'].unique():
                for bus in df[(df['stop_id'] == stop) &
                              (df['routePathId'] == route)]['tmId'].unique():
                    dups = df[
                        (df['stop_id'] == stop) &
                        (df['routePathId'] == route) &
                        (df['tmId'] == bus)].sort_values('request_time', ascending=False)

                    data_cleaned = np.vstack((data_cleaned, dups.to_numpy()[0, :]))

                    for idx, dup in dups.iloc[1:, :].iterrows():
                        if dup['forecast_time'] - data_cleaned[-1, 3] > 600:
                            data_cleaned = np.vstack((data_cleaned, dup.to_numpy()))
                        i += 1
                        if i % 1000 == 0:
                            elapsed = (time() - start) / 60
                            print(f'{i:,} items handled, {elapsed:.2f} min elapsed,')

        df_cleaned = pd.DataFrame(data_cleaned[1:], columns=data_cleaned[0])
        df_cleaned.drop_duplicates(inplace=True)

        elapsed = (time() - start) / 60
        print(f'Cleaner finished at: {asctime()}\n{elapsed:.2f} min elapsed.')
        return df_cleaned


Base.metadata.create_all(engine)
