import csv
from natsort import natsorted
import operator
with open('data/majorrivers.csv', mode = 'r') as csv_file:
    rows = list(csv.reader(csv_file, delimiter=';', quotechar='\"'))

rows = natsorted(rows, key = operator.itemgetter(5), reverse=True)
rows = natsorted(rows, key = operator.itemgetter(4), reverse=True)

with open('data/s_majorrivers.csv', mode = 'w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerows(rows)
