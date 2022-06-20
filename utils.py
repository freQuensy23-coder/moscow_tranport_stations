import signal
import time
from contextlib import contextmanager
from multiprocessing import Queue


def stops_list_to_queue(data: list, queue: Queue = None) -> Queue:
    """Создает очередь из списка координат остановок (tuple)"""
    if queue is None:
        queue = Queue()
    for stop in data:
        coord = stop["stop_id"]
        queue.put(coord)
    return queue


def stops_list_to_stop_id_queue(data: list) -> Queue:
    result = Queue()
    for stop in data:
        coord = stop["stop_id"]
        result.put(coord)
    return result


class TimeoutException(Exception): pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
