import argparse

parser = argparse.ArgumentParser(description='transmetrika')
parser.add_argument('--stops', dest='number_stops', default=-1,
                    help='number of stops to parse', type=int)
parser.add_argument('--threads', dest="threads", type=int, help="Number of threads")