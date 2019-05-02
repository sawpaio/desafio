import requests
from bs4 import BeautifulSoup
import csv
import os
import datetime

html = requests.get(url="https://m.investing.com/crypto/", headers={'User-Agent':'curl/7.52.1'})
#print (html.content)

time = html.headers["Date"][:-4]
#print(time)
datapronta = datetime.datetime.strptime(time, '%a, %d %b %Y %H:%M:%S')
#print(datapronta)

soup = BeautifulSoup(html.content, 'html.parser')
for coin in soup('tr')[1:]:
	lista = coin.get_text().replace('\t', "").split('\n')
#	print(soup)
#	print(lista)

	posi = list(filter(None, lista))
#	print (posi)

	b = csv.writer(open('crypto_timestamp.csv', 'a+'), delimiter =',')
	if os.path.getsize('crypto_timestamp.csv') == 0:
		b.writerow(['code','name', 'priceUSD', 'change24H', 'change7D', 'symbol', 'priceBTC', 'marketCap', 'volume24H', 'totalVolume', 'timestamp'])
		b.writerow([posi[0],posi[1],posi[2],posi[3],posi[4],posi[5],posi[6],posi[7],posi[8],posi[9], datapronta])
	else:
		b.writerow([posi[0],posi[1],posi[2],posi[3],posi[4],posi[5],posi[6],posi[7],posi[8],posi[9], datapronta])
