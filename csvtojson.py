import csv
import json
from pprint import pprint
from datetime import date

f = open('json_fin.csv', 'r')
data_atual = date.today()
a = '"index": {}}'
reader = csv.DictReader(f, fieldnames = ("code","name","priceUSD","change24H","change7D","symbol","priceBTC","priceReal","marketCap","volume24H","totalVolume"))
jsonfile = open('processado_{}.json'.format(data_atual), 'w')

for row in reader:
    json.dump({"index":{}}, jsonfile)
    jsonfile.write('\n')
    json.dump(row, jsonfile)
    jsonfile.write('\n')

