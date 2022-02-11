import logging
import os

THREAD_SLEEP = 1
NUM_THREADS = 55
STATION_CSV = os.getcwd() + "/data.csv"
EXAMPLE_RESULT_FILE = 'example_result.json'
NUMBER_OF_STOPS = 11783
LEVEL = logging.INFO
TIME_LIMIT = 9 * 60  # 9 min
PROXIES_FILE = "proxy.txt"
PATH_TO_DB = f"postgresql:///{os.getenv('db_login')}:{os.getenv('db_pass')}" \
             f"@{os.getenv('db_host')}:{os.getenv('db-port')}"
TOR_RESTART_DELAY: int = 10
headers = {'sec-ch-ua': 'Not;A Brand";v="95", "Google Chrome";v="95", "Chromium";v="95"', 'Host': 'moscowtransport.app',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 '
                         'Safari/537.36'}
DB_ECHO = False
LIMIT_REPEAT: int = 8
