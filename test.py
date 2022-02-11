import unittest

import config
from api import TransAPI
from proxy import FileProxyManager
from station import stops
from config import NUMBER_OF_STOPS, EXAMPLE_RESULT_FILE
from models import Stop


class TestDataValidation(unittest.TestCase):
    def setUp(self):
        with open(EXAMPLE_RESULT_FILE, "r") as f:
            self.example_result = f.read()

    def test_validation(self):
        stop = Stop.parse_raw(self.example_result)
        print(stop)
        self.assertIsNotNone(stop.route_path)


class TestAPIGetStation(unittest.TestCase):
    def setUp(self) -> None:
        self.api = TransAPI()

    def test_get_station(self, api=None):
        api = api or self.api
        station = api.get_station_info(1, 1)
        self.assertEqual(type(station), dict)
        stop = Stop.parse_obj(station)

    def test_proxy(self):
        api = TransAPI(FileProxyManager(file_name=config.PROXIES_FILE))
        self.test_get_station(api=api)
