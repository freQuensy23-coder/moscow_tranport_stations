import os
import time
from random import shuffle
from multiprocessing import Queue

from config import TOR_RESTART_DELAY, PROXY_REUSE
from logging import getLogger

log = getLogger(name="ProxyManagers")


class FileProxyManager:
    """
    Менеджер для проксей из файла
    """
    def __init__(self, file_name):
        """Создаем из списка адресов многопотоковую очередь, чтобы адреса распределялись между потоками"""
        self.proxies = Queue()
        self.thread_proxies = {}

        with open(file_name, "r") as f:
            lines = f.readlines()
            shuffle(lines)

            for line in lines:
                data = line.strip().split(":")  # TODO проверить на соответствие формату файла с прокси
                self.proxies.put({
                    'http': f'http://{data[2]}:{data[3]}@{data[0]}:{data[1]}',
                    'https': f'https://{data[2]}:{data[3]}@{data[0]}:{data[1]}',
                })

    def get_proxy(self, thread_id) -> dict:
        """Метод раздает прокси для каждого нового запроса и меняет адрес после лимита операций"""
        if thread_id not in self.thread_proxies.keys():
            self.thread_proxies[thread_id] = (self.proxies.get(), 1)
            return self.thread_proxies[thread_id][0]
        elif self.thread_proxies[thread_id][1] < PROXY_REUSE:
            self.thread_proxies[thread_id][1] += 1
            return self.thread_proxies[thread_id][0]
        else:
            self.proxies.put(self.thread_proxies[thread_id][0])
            self.thread_proxies[thread_id] = (self.proxies.get(), 1)
            return self.thread_proxies[thread_id][0]

    def _change_ip(self, thread_id) -> dict:  # TODO добавить удаление прокси из файла
        """Метод меняет адрес и удаляет его из очереди, когда тот попадает в бан"""
        self.thread_proxies[thread_id] = (self.proxies.get(), 1)
        return self.thread_proxies[thread_id]


class TorProxy:
    def __init__(self):
        pass

    @staticmethod
    def _change_ip(req_tor):
        log.info("Changing IP...")
        req_tor.new_id()
        time.sleep(TOR_RESTART_DELAY)


class MosTransportBan(Exception):
    """Ваш IP был забанен в мосгортрансе"""
    pass
