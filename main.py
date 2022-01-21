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
from datetime import datetime
from cl_arguments import parser

log = getLogger()
logging.basicConfig(filename="parser.log",
                    format='%(asctime)s %(levelname)s %(message)s ', level=logging.DEBUG, filemode="w")
session = sessionmaker(bind=engine)()

args = parser.parse_args()
log.debug(f"Command line args: {args}")


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
    time_start = datetime.now()
    log.info(f"Started at {time_start}.")
    api = TransAPI()
    stops_list = list(stops())

    if args.number_stops != -1:
        stops_list = stops_list[:args.number_stops]

    stops = Queue()
    for stop in stops_list:
        coord = lon, lat = stop["Lon"], stop["Lat"]
        stops.put(coord)

    NUM_THREADS = args.threads or NUM_THREADS
    NUM_THREADS = min(len(stops_list) - 1, NUM_THREADS) # TODO Исправить баг с переизбытком потоков
    log.debug(f"Creating {NUM_THREADS} threads")

    threads = []
    for i in range(NUM_THREADS):
        t = threading.Thread(target=thread_job, name=f"{i}")
        t.start()
        threads.append(t)

    for t in threads:
        log.debug(f"Waiting for Thread {t.name}")
        t.join()
        log.debug(f"Thread {t.name} finished")

    time_req = datetime.now()
    log.info(f"Перехожу к сохранению данных. Загрузка заняла {time_req - time_start}")
    session.commit()
    time_save = datetime.now()
    log.info(
        f"Отработал. Сохранение в бд заняло {time_save - time_req}. Общее время работы этого запуска: {time_save - time_start}")
