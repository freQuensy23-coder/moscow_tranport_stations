import logging

NUM_THREADS = 55
STATION_CSV = "/home/frequensy/MosTransParser/moscow_tranport_stations/data.csv"
EXAMPLE_RESULT_FILE = 'example_result.json'
NUMBER_OF_STOPS = 11783
LEVEL = logging.INFO
TIME_LIMIT = 9 * 60 # 9 min
PROXIES =  {
'http': 'http://lum-customer-hl_20aeee3d-zone-data_center-ip-157.119.42.115:1mpxba1ot4sf@zproxy.lum-superproxy.io:22225',
'https': 'https://lum-customer-hl_20aeee3d-zone-data_center-ip-157.119.42.115:1mpxba1ot4sf@zproxy.lum-superproxy.io:22225'
}
PROXIES_FILE = "35proxy.txt"
