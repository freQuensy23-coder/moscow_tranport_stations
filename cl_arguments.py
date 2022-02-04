import argparse
import logging
import config

parser = argparse.ArgumentParser(description='transmetrika')
parser.add_argument('--stops', dest='number_stops', default=-1,
                    help='number of stops to parse', type=int)
parser.add_argument('--threads', dest="threads", type=int, help="Number of threads", default=config.NUM_THREADS)
parser.add_argument(
    '-d', '--debug',
    help="Print lots of debugging statements",
    action="store_const", dest="loglevel", const=logging.DEBUG,
    default=logging.INFO,
)
parser.add_argument('-tl', "--time_limit",
                    help="Limit time of script work in seconds",
                    type=int, dest="time_limit", default=config.TIME_LIMIT
                    )
parser.add_argument("--stations", help="csv file with station coords", type=str, dest="stations_csv",
                    default=config.STATION_CSV)
parser.add_argument('--proxy_file', help='file with proxy data', type=str, dest="proxy_file")
parser.add_argument('--proxy', help='use proxy from config', action='store_const', dest="proxy_file",
                    const=config.PROXIES_FILE)
parser.add_argument('--tor', help='use_tor', action='store_true', dest='tor')