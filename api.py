import requests as req
import logging
from random import randint

log = logging.getLogger("TransAPI")
headers = {'User-Agent': f'My User Agent 1.1', 'From': 'domain.com'}


class TransAPI:
    def __init__(self, requester=req):
        self.requester = requester

    @staticmethod
    def get_link(lon, lat) -> str:
        return f"https://moscowtransport.app/api/qr-stop/undefined/stop?p={lon}, {lat}"

    def get_station_info(self, lon, lat) -> dict:
        link = self.get_link(lon, lat)
        r = self.requester.get(link, headers=headers)
        station_data = r.json()
        log.debug(station_data)
        log.info(f"Get information about station {station_data.get('name')}, ID: {station_data.get('id')}")
        return station_data
