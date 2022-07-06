from datetime import datetime
import logging
from logging import getLogger
import queue
import threading

from sqlalchemy.orm import sessionmaker

from api.api import TorTransAPI, TransAPI
from api.proxy import FileProxyManager, TorProxyManager
from cl_arguments import parser
from db.db import engine
from station import stops_coord
from utils import stops_list_to_queue

log = getLogger()
args = parser.parse_args()
logging.basicConfig(filename="parser.log", format='%(asctime)s %(levelname)s %(message)s ',
                    level=args.loglevel, filemode="a")
log.debug(f"Command line args: {args}")
session = sessionmaker(bind=engine)()


def parser_thread():
    """Поток получает остановки из очереди и занимается их обработкой"""
    while True:
        try:
            log.debug(f'{stops_queue.unfinished_tasks=}')
            stop_id = stops_queue.get(block=False)
            stops_queue.task_done()
        except queue.Empty:
            log.debug(f"Finish. Queue is empty. Thread {threading.current_thread().name}")
            return
        log.debug(f"Thread {threading.current_thread().name} is working with {stop_id}")

        api.thread_runner(stop_id, session)


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
        proxy = TorProxyManager()
        api = TorTransAPI(proxy)
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
