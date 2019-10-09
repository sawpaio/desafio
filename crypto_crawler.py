import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime
import time

html = requests.get(url="https://m.investing.com/crypto/", headers={'User-Agent':'curl/7.52.1'})
#print (html.content)
cwd = os.getcwd()
now = datetime.now()
datapronta = datetime.timestamp(now)
#print(datapronta)
ts = time.time()

soup = BeautifulSoup(html.content, 'html.parser')
for coin in soup('tr')[1:]:
	lista = coin.get_text().replace('\t', "").split('\n')
#	print(soup)
#	print(lista)

	posi = list(filter(None, lista))

	b = csv.writer(open(cwd + '/lucasSampaio/crawler_crypto/crypto_{}.csv'.format(ts), 'a+') , delimiter =',')
	if os.path.getsize(cwd +'/lucasSampaio/crawler_crypto/crypto_{}.csv'.format(ts)) == 0:
		b.writerow(['code','name', 'priceUSD', 'change24H', 'change7D', 'symbol', 'priceBTC', 'marketCap', 'volume24H', 'totalVolume', 'timestamp'])
		b.writerow([posi[0],posi[1],posi[2],posi[3],posi[4],posi[5],posi[6],posi[7],posi[8],posi[9], datapronta])
	else:
		b.writerow([posi[0],posi[1],posi[2],posi[3],posi[4],posi[5],posi[6],posi[7],posi[8],posi[9], datapronta])
