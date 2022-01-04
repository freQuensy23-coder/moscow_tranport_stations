import requests as req


class TransAPI:
    def __init__(self, requester=req):
        self.requester = requester

    @staticmethod
    def get_link(lon, lat) -> str:
        return f"https://moscowtransport.app/api/qr-stop/undefined/stop?p={lon}, {lat}"

    def get_station_info(self, lon, lat) -> dict:
        link = self.get_link(lon, lat)
        r = req.get(link)
        station_data = r.json()
        return station_data
