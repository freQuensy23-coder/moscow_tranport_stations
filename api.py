import requests as req
import logging
from random import randint

log = logging.getLogger("TransAPI")
headers = {'sec-ch-ua': 'Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"', 'Host':'moscowtransport.app', 'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}


class TransAPI:
    def __init__(self, requester=req):
        self.requester = requester

    @staticmethod
    def get_link(lon, lat) -> str:
        return f"https://moscowtransport.app/api/qr-stop/1111/stop?p={lon}, {lat}"

    def get_station_info(self, lon, lat) -> dict:
        link = self.get_link(lon, lat)
        r = self.requester.get(link, headers=headers)
        station_data = r.json()
        log.debug(station_data)
        log.info(f"Get information about station {station_data.get('name')}, ID: {station_data.get('id')}")
        return station_data
