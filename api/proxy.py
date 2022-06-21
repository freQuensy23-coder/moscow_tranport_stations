import os
import time
from random import choice

from config import TOR_RESTART_DELAY
from logging import getLogger

log = getLogger(name="ProxyManagers")


class ProxyManager:
    def __init__(self, proxies: list):
        self._proxies = proxies

    def get_proxy(self) -> dict:
        """Method should return dict with available method as keys and proxy data as values. Ex:
        {'http': f'http://{login}:{pass}@{ip}:{port}',
         'https': f'https://{login}:{pass}@{ip}:{port}'}
        """
        proxy = choice(self._proxies)
        log.debug(f"{proxy} selected by file proxy manager")
        return proxy

    @staticmethod
    def _change_ip(*args):
        """Method calls if requests from ip is not working."""
        log.info("Changing IP...")
        # TODO добавлять IP во временную отлегу
        pass


class FileProxyManager(ProxyManager):
    def __init__(self, file_name):
        f = open(file_name, "r")
        proxies = []
        for line in f:
            data = line.strip().split(":")  # TODO сделать читаемее
            proxies.append({
                'http': f'http://{data[2]}:{data[3]}@{data[0]}:{data[1]}',
                'https': f'https://{data[2]}:{data[3]}@{data[0]}:{data[1]}',
            }
            )
        super().__init__(proxies)
        f.close()


class TorProxy(ProxyManager):
    def __init__(self, port=9050, ip='127.0.0.1'):
        proxy = {'https': f'socks5://{ip}:{port}',
                 'http': f'socks5://{ip}:{port}'}
        super().__init__([proxy])

    @staticmethod
    def _change_ip(*args):
        log.info("Changing IP...")
        os.system("sudo service tor restart")
        time.sleep(TOR_RESTART_DELAY)


class MosTransportBan(Exception):
    """Ваш IP был забанен в мосгортрансе"""
    pass