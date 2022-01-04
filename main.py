from db.db import engine
from models import Stop
from station import stops
from api import TransAPI
from sqlalchemy.orm import sessionmaker
import threading
from multiprocessing import Queue
from logging import getLogger
import logging
from config import NUM_THREADS

log = getLogger()
logging.basicConfig(level=logging.INFO)
session = sessionmaker(bind=engine)()


def thread_job():
    """Поток получает остановки из очереди и занимается их обработкой"""
    coord = stops.get()
    while coord is not None:
        log.info(f"Parse station at {coord}")
        lon, lat = coord
        stop = Stop.parse_obj(api.get_station_info(lon, lat))
        stop.save(session, commit=False)
        coord = stops.get()


if __name__ == "__main__":
    api = TransAPI()
    stops_list = list(stops())
    stops = Queue()
    for stop in stops_list[:150]:
        coord = lon, lat = stop["Lon"], stop["Lat"]
        stops.put(coord)

    threads = []
    for i in range(NUM_THREADS):
        t = threading.Thread(target=thread_job, name=f"{i}")
        t.start()

    for t in threads:
        t.join()

    session.commit()
