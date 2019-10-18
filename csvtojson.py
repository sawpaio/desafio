import csv
import json
from pprint import pprint
f = open('join_fin.csv', 'r')
a = '"index": {}}'
reader = csv.DictReader(f, fieldnames = ("code","name","priceUSD","change24H","change7D","symbol","priceBTC","priceReal","marketCap","volume24H","totalVolume"))
jsonfile = open('file.json', 'w')

for row in reader:
    json.dump({"index":{}}, jsonfile)
    jsonfile.write('\n')
    json.dump(row, jsonfile)
    jsonfile.write('\n')

