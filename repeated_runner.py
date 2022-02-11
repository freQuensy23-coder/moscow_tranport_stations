import os
import time
from datetime import datetime

import telegram_send

run_script = "sudo /home/frequensy/MosTransParser/moscow_tranport_stations/venv/bin/python3.9 " \
             "/home/frequensy/MosTransParser/moscow_tranport_stations/main.py --stations  " \
             "/home/frequensy/MosTransParser/moscow_tranport_stations/uniq_stops.csv -d --proxy_file proxy.txt "
restart_tor = "sudo service tor reload"


def telelog(msg: str):
    """Log to telegram"""
    print(f"{msg}")
    telegram_send.send(messages=[msg])


while True:
    if (datetime.now().hour + 3) % 24 < 5:
        telelog("sleep")
        time.sleep(60 * 60)
    try:
        telelog(f"Started in {datetime.now()}")
        os.system(run_script)
    except:
        telelog(f"Smth went wrong in {datetime.now()}")
    time.sleep(25)
