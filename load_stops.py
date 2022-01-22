import logging
from db.db import engine
from models import Stop
from station import stops
from api import TransAPI
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm
from logging import basicConfig

api = TransAPI()
session = sessionmaker(bind=engine)()
stops_list = list(stops())
basicConfig(level=logging.DEBUG, filemode="w", filename="load_stops.log")

for stop in tqdm(stops_list):
    coord = lon, lat = stop["Lon"], stop["Lat"]
    stop = Stop.parse_obj(api.get_station_info(lon, lat))
    stop.save_stop(session)

session.commit()
