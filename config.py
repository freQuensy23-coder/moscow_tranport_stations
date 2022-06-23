import logging
import os

THREAD_SLEEP = 1 # Задержка потока
NUM_THREADS = 55 # Количество создаваемы потоков
STATION_CSV = os.getcwd() + "/stop.csv" # CSV файл с информацией об остановкам по которым делаются запросы

DB_CONNECTION_STRING = f"postgresql://{os.getenv('db_login')}:{os.getenv('db_pass')}" \
             f"@{os.getenv('db_host')}:{os.getenv('db_port')}/transmetrika" # Параметры БД
DB_ECHO = True # Выводить ли в консоль SQL запросы


PROXIES_FILE = "proxy.txt" # файл с прокси по умолчанию
TOR_RESTART_DELAY: int = 10 # задержка после перезагружки сервиса тор

LEVEL = logging.INFO # Уровень логгирования в обычном режими
TIME_LIMIT = 9 * 60  # 9 min Лимит времени работы программы


EXAMPLE_RESULT_FILE = 'example_result.json' # Пример ответа от сервера
NUMBER_OF_STOPS = 11783


headers = {'sec-ch-ua': 'Not;A Brand";v="95", "Google Chrome";v="95", "Chromium";v="95"', 'Host': 'moscowtransport.app',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 '
                         'Safari/537.36'} # Headers для запроса

LIMIT_REPEAT = 4 # Максимальнео количество запросов на одну остановку
DELAY_STOPS = 60 * 6 # Задеркжа перед повторным опросом
