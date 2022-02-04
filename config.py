import logging
import os

NUM_THREADS = 55
STATION_CSV = os.getcwd() + "/data.csv"
EXAMPLE_RESULT_FILE = 'example_result.json'
NUMBER_OF_STOPS = 11783
LEVEL = logging.INFO
TIME_LIMIT = 9 * 60  # 9 min
PROXIES_FILE = "35proxy.txt"
PATH_TO_DB = "sqlite:///" + os.getcwd() + "/db/forecast.db"
