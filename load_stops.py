import logging
import time
from logging import basicConfig
from threading import Thread

import progressbar
from sqlalchemy.orm import sessionmaker

from api import TransAPI, MosTransportBan, TorProxy
from db.db import engine
from models import Stop
from station import stops
from utils import stops_list_to_queue

proxy = TorProxy()
api = TransAPI(proxy)
session = sessionmaker(bind=engine)()
stops_list = list(stops(f_name="data.csv"))
basicConfig(level=logging.DEBUG, filemode="a", filename="load_stops.log")
parsed_stops = 0
max_stops = len(stops_list)
queue = stops_list_to_queue(stops_list)


def parse_stop():
    global queue, session, parsed_stops
    while not queue.empty():
        coord = lon, lat = queue.get()
        stop = None
        while stop is None:
            try:
                stop = Stop.parse_obj(api.get_station_info(lon, lat))
            except MosTransportBan:
                api.change_ip()
        parsed_stops += 1
        stop.save_stop(session, commit=False)
    return True


threads = []
N = 51
for i in range(N):
    t = Thread(name=f"{i}", target=parse_stop)
    t.start()
    threads.append(t)

bar = progressbar.ProgressBar(max_value=max_stops)
while parsed_stops < max_stops:
    bar.update(parsed_stops)
    time.sleep(1)

for t in threads:
    log.info("Check threads")
    t.join()

session.commit()
