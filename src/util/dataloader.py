import csv

def read_rivers_csv(path):
    rivers = {}
    with open(path) as csv_file:
        rows = csv.reader(csv_file, delimiter=';')
        for row in rows:
            rivers[row[0]] = {'line': row[1], 'area': row[2]}
    return rivers