import unittest
from station import stops
from config import NUMBER_OF_STOPS, EXAMPLE_RESULT_FILE
from models import Stop


class TestStopListUoloading(unittest.TestCase):
    def test_stop_name(self):
        name = list(stops())[2]["Name"]
        self.assertEqual(name, "«ВКНЦ», 3-я Черепковская улица (27)")

    def test_stops_all_upload(self):
        l = list(stops())
        self.assertEqual(len(l), NUMBER_OF_STOPS)


class TestDataValidation(unittest.TestCase):
    def setUp(self):
        with open(EXAMPLE_RESULT_FILE, "r") as f:
            self.example_result = f.read()

    def test_validation(self):
        stop = Stop.parse_raw(self.example_result)
        print(stop)
        self.assertIsNotNone(stop.route_path)

