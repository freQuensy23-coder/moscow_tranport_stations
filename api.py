import requests as req
import logging
from random import choice
from config import TOR_RESTART_DELAY, headers

log = logging.getLogger("TransAPI")

class TransAPI:
    def __init__(self, proxy_manager=None, requester=req):
        self.requester = requester
        self.proxy_manager = proxy_manager

    @staticmethod
    def get_link(lon, lat) -> str:
        return f"https://moscowtransport.app/api/qr-stop/1111/stop?p={lon},{lat}"

    def get_station_info(self, lon, lat) -> dict:
        link = self.get_link(lon, lat)
        if self.proxy_manager is None:
            r = self.requester.get(link, headers=headers)
        else:
            proxy = self.proxy_manager.get_proxy()
            r = self.requester.get(link, headers=headers, proxies=proxy)
        if r.content == b"":
            log(f"Banned in MGT. Current ip is {self.get_ip()}")
            raise MosTransportBan("You have been banned")
        station_data = r.json()
        log.debug(station_data)
        log.debug(f"Get information about station {station_data.get('name')}, ID: {station_data.get('id')}")
        return station_data

    def get_ip(self):
        link = "https://ifconfig.me"
        self.make_req(link)
        return r.content

    def change_ip(self):
        if self.proxy_manager and "_change_ip" in dir(self.proxy_manager):
            self.proxy_manager._change_ip()
            log.info(f"Ip changed, new ip is {self.get_ip()}")
        else:
            log.warn("Trying to change IP but proxymanager didn't selected ot does not allowed to do this")
            raise MosTransportBan("Trying to change IP but proxymanager is now allowed to do this")

    def make_req(self, link, **kwargs):
        if self.proxy_manager is None:
            r = self.requester.get(link, *kwargs)
        else:
            proxy = self.proxy_manager.get_proxy()
            r = self.requester.get(link, proxies=proxy, *kwargs)
        return r


class FileProxyManager:
    def __init__(self, file_name):
        f = open(file_name, "r")
        self._proxies = []
        for line in f:
            data = line.strip().split(":")
            self._proxies.append({
                'http': f'http://{data[2]}:{data[3]}@{data[0]}:{data[1]}',
                'https': f'https://{data[2]}:{data[3]}@{data[0]}:{data[1]}',
            }
            )
        f.close()

    def get_proxy(self):
        return choice(self._proxies)


class TorProxy:
    def __init__(self, port=9050, ip='127.0.0.1'):
        self.proxy = {'https': f'socks5://{ip}:{port}',
                      'http': f'socks5://{ip}:{port}'}

    def get_proxy(self):
        return self.proxy

    @staticmethod
    def _change_ip():
        log.info("Changing IP...")
        os.system("sudo service tor restart")
        time.sleep(TOR_RESTART_DELAY)


class MosTransportBan(Exception):
    """Наш IP был забанен в мосгортрансе"""
    pass

