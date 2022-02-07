import os
import time
from datetime import datetime

run_script = "sudo /home/frequensy/MosTransParser/moscow_tranport_stations/venv/bin/python3.9 " \
             "/home/frequensy/MosTransParser/moscow_tranport_stations/main.py --stations  " \
             "/home/frequensy/MosTransParser/moscow_tranport_stations/trams.csv -d --proxy_file proxy.txt "
restart_tor = "sudo service tor reload"

while True:
    if (datetime.now().hour + 3) % 24 < 5:
        print("sleep")
        time.sleep(60 * 60)
    try:
        print(f"Started in {datetime.now()}")
        os.system(run_script)
    except:
        print(f"Smth went wrong at {time.time()}")
    os.system(restart_tor)
    time.sleep(2 * 60)
