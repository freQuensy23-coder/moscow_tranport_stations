import time
from multiprocessing import Queue


def stops_list_to_queue(data: list) -> Queue:
    result = Queue()
    for stop in data:
        coord = stop["Lon"], stop["Lat"]
        result.put(coord)
    return result

