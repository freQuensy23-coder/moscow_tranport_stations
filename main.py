import requests
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
logging.basicConfig(level=logging.DEBUG)
session = sessionmaker(bind=engine)()


def thread_job():
    """Поток получает остановки из очереди и занимается их обработкой"""
    while not stops.empty():
        coord = stops.get()
        log.debug(f"Thread is working with {coord}")
        lon, lat = coord
        stop = Stop.parse_obj(api.get_station_info(lon, lat))
        stop.save(session, commit=False)
    log.debug("Thread finish working")
    return None


if __name__ == "__main__":
    api = TransAPI()
    stops_list = list(stops())
    stops = Queue()
    for stop in stops_list[:950]:
        coord = lon, lat = stop["Lon"], stop["Lat"]
        stops.put(coord)

    threads = []
    for i in range(NUM_THREADS):
        t = threading.Thread(target=thread_job, name=f"{i}")
        t.start()
        threads.append(t)

    for t in threads:
        log.debug(f"Waiting for Thread {t.name}")
        t.join()
        log.debug(f"Thread {t.name} finished")

    session.commit()
