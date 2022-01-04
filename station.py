import csv
from config import STATION_CSV as f_name


def stops():
  """Генератор возвращающий по очереди информацию о автобусных остановках"""
  with open(f_name, 'r') as f:
      reader = csv.DictReader(f)
      for row in reader:
        yield row
