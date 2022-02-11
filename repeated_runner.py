import os
import time
from datetime import datetime

import telegram_send

run_script = "/home/frequensy/MosTransParser/moscow_tranport_stations/venv/bin/python3.9 " \
             "/home/frequensy/MosTransParser/moscow_tranport_stations/main.py --stations  " \
             "/home/frequensy/MosTransParser/moscow_tranport_stations/uniq_stops.csv -d --proxy_file proxy.txt "
restart_tor = "sudo service tor reload"


def telelog(msg: str):
    """Log to telegram"""
    print(f"{msg}")
    telegram_send.send(messages=[msg])


sleep = True
while True:
    t0 = time.time()
    if sleep and (datetime.now().hour + 3) % 24 < 5:
        telelog("sleep")
        time.sleep(60 * 60)
    try:
        telelog(f"Started at {datetime.now()}")
        os.system(run_script)
    except:
        telelog(f"Smth went wrong at {datetime.now()}")
    time.sleep(max(0, int(3 * 60 - (time.time() - t0))))
