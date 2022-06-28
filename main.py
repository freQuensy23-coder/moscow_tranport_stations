import queue

from config import LIMIT_REPEAT
from db.db import engine
from models import Stop
from station import stops_coord
from api.api import TransAPI, MosTransportBan
from api.proxy import FileProxyManager, TorProxy
from sqlalchemy.orm import sessionmaker
import threading
from logging import getLogger
import logging
from datetime import datetime
from cl_arguments import parser
from utils import stops_list_to_queue

log = getLogger()

args = parser.parse_args()
log.debug(f"Command line args: {args}")

logging.basicConfig(filename="parser.log", format='%(asctime)s %(levelname)s %(message)s ',
                    level=args.loglevel, filemode="a")
session = sessionmaker(bind=engine)()


def parser_thread():
    """Поток получает остановки из очереди и занимается их обработкой"""
    while True:
        try:
            stop_id = stops_queue.get(block=False)
        except queue.Empty:
            log.debug("Finish. Queue is empty.")
            return None
        log.debug(f"Thread is working with {stop_id}")
        station_info = None
        repeat = 0
        while station_info is None:
            repeat += 1
            if repeat >= LIMIT_REPEAT:  # TODO Вынести всю вот эту логику в API если куча запросов не прошло надо прекращать пытаться
                log.warning("Unable to get valid station data")
                raise MosTransportBan("Unable to get valid station data")
            try:
                station_info = api.get_station_info(stop_id=stop_id)
                log.debug(f"Parsing station info: {station_info}")
                stop = Stop.parse_obj(station_info)
            except MosTransportBan:
                log.warning("Changing ip")
                api.change_ip()
            except Exception as e:
                log.exception(e)
                log.warning(f"{e}")
                log.warning("Changing ip..")
                api.change_ip()
                station_info = None

        stop.save_forecast(session, commit=False) # TODO
    log.debug("Thread finish working")
    return None


def wait_for_threads():
    global stops_list, NUM_THREADS, stops_queue, threads
    for worker in threads:
        worker.join()


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

    NUM_THREADS = args.threads
    NUM_THREADS = min(len(stops_list) - 1, NUM_THREADS)
    log.info(f"Creating {NUM_THREADS} threads")

    if args.number_stops != -1:
        stops_list = stops_list[:args.number_stops]
    stops_queue = stops_list_to_queue(stops_list)

    threads = []
    for i in range(NUM_THREADS):
        t = threading.Thread(target=parser_thread, name=f"{i}")
        t.start()
        threads.append(t)
    wait_for_threads()
    session.commit()
    log.info("Done!")
