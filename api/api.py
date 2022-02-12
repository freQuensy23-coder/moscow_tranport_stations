import requests as req
import logging
from fake_headers import Headers

from api.proxy import MosTransportBan

log = logging.getLogger("TransAPI")
h = Headers()


class TransAPI:
    def __init__(self, proxy_manager=None, requester=req):
        self.requester = requester
        self.proxy_manager = proxy_manager

    @staticmethod
    def get_link(**kwargs) -> str:
        if kwargs.get("lon") and kwargs.get("lat"):
            lon, lat = kwargs["lon"], kwargs['lat']
            return f"https://moscowtransport.app/api/qr-stop/1111/stop?p={lon},{lat}"
        else:
            stop_id = kwargs["stop_id"]
            return f"https://moscowtransport.app/api/stop_v2/{stop_id}"

    def get_station_info(self, **kwargs) -> dict:
        if kwargs.get('lon'):
            lon, lat = kwargs.get("lon"), kwargs.get("lat")
            link = self.get_link(**kwargs)
            r = self.make_req(link)
            if r.content == b"":
                log.warning(f"Banned in MGT. Current ip is {self.get_ip()}")
                raise MosTransportBan("You have been banned")
            station_data = r.json()
            log.debug(f"API get station data {station_data} for station {(lon, lat)}. Link = {link}")
            log.debug(f"Get information about station {station_data.get('name')}, ID: {station_data.get('id')}")
            return station_data

    def get_ip(self):
        # link = "https://ifconfig.me/ip"
        # r = self.make_req(link)
        # return r.content
        return "11"

    def change_ip(self):
        if self.proxy_manager and "_change_ip" in dir(self.proxy_manager):
            self.proxy_manager._change_ip()
            log.info(f"Ip changed, new ip is {self.get_ip()}")
        else:
            log.warning("Trying to change IP but proxymanager didn't selected ot does not allowed to do this")
            raise MosTransportBan("Trying to change IP but proxymanager is now allowed to do this")

    def make_req(self, link, **kwargs):
        if self.proxy_manager is None:
            r = self.requester.get(link, headers=h.generate(), *kwargs)
        else:
            proxy = self.proxy_manager.get_proxy()
            log.debug(f"Making req with proxy {proxy}")
            r = self.requester.get(link, proxies=proxy, headers=h.generate(), *kwargs)
        return r


