from db.db import engine
from models import Stop
from station import stops as stops_coord
from api import TransAPI, FileProxyManager, TorProxy
from sqlalchemy.orm import sessionmaker
import threading
from multiprocessing import Queue
from logging import getLogger
import logging
from datetime import datetime
from cl_arguments import parser
from time_limit import time_limit, TimeoutException

log = getLogger()

args = parser.parse_args()
log.debug(f"Command line args: {args}")

logging.basicConfig(filename="parser.log", format='%(asctime)s %(levelname)s %(message)s ',
                    level=args.loglevel, filemode="w")
session = sessionmaker(bind=engine)()


def thread_job():
    """Поток получает остановки из очереди и занимается их обработкой"""
    while not stops.empty():
        coord = stops.get()
        log.debug(f"Thread is working with {coord}")
        lon, lat = coord
        station_info = api.get_station_info(lon, lat)
        log.debug(f"{station_info}")
        stop = Stop.parse_obj(station_info)
        stop.save_forecast(session, commit=False)
    log.debug("Thread finish working")
    return None


def main():
    global stops_list, NUM_THREADS, stops
    if args.number_stops != -1:
        stops_list = stops_list[:args.number_stops]

    stops = Queue()
    for stop in stops_list:
        coord = stop["Lon"], stop["Lat"]
        stops.put(coord)

    NUM_THREADS = args.threads
    NUM_THREADS = min(len(stops_list) - 1, NUM_THREADS)
    log.info(f"Creating {NUM_THREADS} threads")

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


if __name__ == "__main__":
    time_start = datetime.now()
    log.info(f"Started at {time_start}.")

    if args.proxy_file:
        file_proxy = FileProxyManager(args.proxy_file)
        api = TransAPI(file_proxy)
    elif args.tor:
        proxy = TorProxy()
        api = TransAPI(proxy)
    else:
        api = TransAPI()

    stops_list = list(stops_coord(f_name=args.stations_csv))

    try:
        with time_limit(args.time_limit):
            main()
    except TimeoutException as e:
        log.warning("TIME LIMIT")

