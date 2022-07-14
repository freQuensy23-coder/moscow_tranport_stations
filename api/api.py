import logging
import threading

import requests as req
from fake_headers import Headers
from requests_tor import RequestsTor as req_tor

from api.proxy import MosTransportBan
from config import PROXY_REUSE, TOR_PASSWORD, LIMIT_REPEAT, NUM_THREADS
from models import Stop

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

    def thread_runner(self, stop_id, session):
        station_info = None
        repeat = 0
        while station_info is None:
            repeat += 1
            if repeat >= LIMIT_REPEAT:
                log.warning("Unable to get valid station data")
                raise MosTransportBan("Unable to get valid station data")
            try:
                station_info = self.get_station_info(stop_id=stop_id)
                log.debug(f"Parsing station info: {station_info}")
                stop = Stop.parse_obj(station_info)
            except MosTransportBan:
                log.warning("Changing ip")
                self.change_ip()
            except Exception as e:
                log.exception(e)
                log.warning(f"{e}")
                log.warning("Changing ip..")
                self.change_ip()
                station_info = None
        stop.save_forecast(session, commit=False)

    def get_station_info(self, **kwargs) -> dict:
        if kwargs.get('lon'):
            lon, lat = kwargs.get("lon"), kwargs.get("lat")
            link = self.get_link(**kwargs)
            r = self.make_req(link)
            if r.content == b"":
                log.warning(f"Banned in MGT. Current ip is {self.current_ip()}")
                raise MosTransportBan("You have been banned")
            station_data = r.json()
            log.debug(f"API get station data {station_data} for station {(lon, lat)}. Link = {link}")
            log.debug(f"Get information about station {station_data.get('name')}, ID: {station_data.get('id')}")
        elif kwargs.get("stop_id"):
            stop_id = kwargs["stop_id"]
            link = self.get_link(**kwargs)
            r = self.make_req(link)
            if r.content == b"":
                log.warning(f"Banned in MGT. Current ip is {self.current_ip()}")
                raise MosTransportBan("You have been banned")
            station_data = r.json()
            log.debug(f"API get station data {station_data} for station {stop_id}. Link = {link}")
            log.debug(f"Get information about station {station_data.get('name')}, ID: {station_data.get('stop_id')}")
        return station_data

    def current_ip(self):
        # r = self.make_req('https://api.ipify.org')
        # return r.content
        pass

    def change_ip(self):
        """Меняет прокси IP."""
        if self.proxy_manager and "change_proxy" in dir(self.proxy_manager):
            self.proxy_manager.change_proxy(threading.get_ident())
            log.info(f"Ip changed, new ip is {self.current_ip()}")
        else:
            log.warning("Trying to change IP but proxymanager didn't selected or does not allowed to do this")
            raise MosTransportBan("Trying to change IP but proxymanager is not allowed to do this")

    def make_req(self, link, **kwargs):
        if self.proxy_manager is None:
            r = self.requester.get(link, headers=h.generate(), *kwargs)
        else:
            thread_id = threading.get_ident()
            proxy = self.proxy_manager.get_proxy(thread_id)
            log.debug(f"Making req with proxy {proxy}")
            r = self.requester.get(link, proxies=proxy, headers=h.generate(), *kwargs)
        return r


class TorTransAPI(TransAPI):
    def __init__(self, proxy_manager=None, num_threads=NUM_THREADS):
        if num_threads <= 50:
            self.PORTS = [i for i in range(9000, 9000 + num_threads)]
            log.info(f'Using {len(self.PORTS)} SOCKS proxy addresses')
        else:
            self.PORTS = [i for i in range(9000, 9050)]
            log.info(f'Number of threads exceeds number of SOCKS ports. Using {len(self.PORTS)} unique addresses instead')

        self.proxy_manager = proxy_manager
        self.requester = req_tor(tor_ports=self.PORTS,
                                 tor_cport=9051,
                                 password=TOR_PASSWORD,
                                 autochange_id=PROXY_REUSE,
                                 verbose=True)

    def change_ip(self):
        if self.proxy_manager and "change_proxy" in dir(self.proxy_manager):
            self.proxy_manager.change_proxy(self.requester)
            log.info(f"Ip changed, new ip is {self.current_ip()}")
        else:
            log.warning("Trying to change IP but proxymanager didn't selected or does not allowed to do this")
            raise MosTransportBan("Trying to change IP but proxymanager is not allowed to do this")

    def make_req(self, link, **kwargs):
        r = self.requester.get(link, headers=h.generate(), *kwargs)
        return r
