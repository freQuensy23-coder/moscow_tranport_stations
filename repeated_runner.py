import os
import time
from datetime import datetime


run_script = "sudo /home/frequensy/MosTransParser/moscow_tranport_stations/venv/bin/python3.9 /home/frequensy/MosTransParser/moscow_tranport_stations/main.py --stations  /home/frequensy/MosTransParser/moscow_tranport_stations/trams.csv -d --tor"
restart_tor = "sudo service tor reload"

while True:
    if (datetime.now().hour + 3 )%24 < 5:
        print("sleep")
        time.sleep(60*60)
    try:
        print(f"Запустился в {datetime.now()}")
        os.system(run_script)
    except:
        print(f"SMTH WRONG {time.now()}")
    os.system(restart_tor)
    time.sleep(2*60)
    
