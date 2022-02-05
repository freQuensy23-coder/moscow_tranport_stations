import requests as req
import logging
from random import choice

log = logging.getLogger("TransAPI")
headers = {'sec-ch-ua': 'Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"', 'Host': 'moscowtransport.app',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}


class TransAPI:
    def __init__(self, proxy_manager=None, requester=req):
        self.requester = requester
        self.proxy_manager = proxy_manager

    @staticmethod
    def get_link(lon, lat) -> str:
        return f"http://moscowtransport.app/api/qr-stop/1111/stop?p={lon},{lat}"

    def get_station_info(self, lon, lat) -> dict:
        link = self.get_link(lon, lat)
        if self.proxy_manager is None:
            r = self.requester.get(link, headers=headers)
        else:
            proxy = self.proxy_manager.get_proxy()
            r = self.requester.get(link, headers=headers, proxies=proxy)

        station_data = r.json()
        log.debug(station_data)
        log.debug(f"Get information about station {station_data.get('name')}, ID: {station_data.get('id')}")
        return station_data


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
