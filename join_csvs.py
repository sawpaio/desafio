################################
##############join_csv.py
############ Lucas Sampaio de Melo
####### 18/10/2019

from datetime import datetime, timedelta, date
from elasticsearch import Elasticsearch
import glob
import csv  
import json  
import os
import requests
import pandas as pd

cwd = os.getcwd()

#Manipulação dos arquivos relacionados ao Dolar.
dolar = glob.iglob(cwd + '/crawler_dolar/*.csv')
col = []
for filedolar in dolar:
    df2 = pd.read_csv(filedolar, index_col=None, header=0)
    val = df2['value'].values[0]
del df2['timestamp']
dol = df2.to_csv(cwd +'/crawler_crypto/consolidados/ok.csv')

#Abertura dos csv's gerados pelo py de Crypto.
all_files = glob.iglob(cwd + '/crawler_crypto/*.csv')

li = []
for file in all_files:
    df = pd.read_csv(file, index_col=None, header=0)
    li.append(df)

df = pd.concat(li, axis=0, ignore_index=True)
del df['marketCap']
del df['change7D']
del df['totalVolume']
df.to_csv(cwd +'/crawler_crypto/consolidados/join_fin.csv')
a = []

#Adiciona o campo priceReal que é multiplicado pelo valor do dolar no dia.
r = open(cwd + '/crawler_crypto/consolidados/join_fin.csv')
lines = r.readlines()[1:]
final = []
for teste in lines:
    pos = teste.split(',')[3].replace('"', '')
    conta = float(pos) * float(val)
    final.append(conta)
df.insert(3 , 'priceReal', final)
df.to_csv(cwd +'/crawler_crypto/consolidados/join_fin.csv', index=False)
# print(df)

data = date.today() - timedelta(days=1)
data.strftime('%Y-%m-%d')
filefinal = open(cwd +'/crawler_crypto/consolidados/join_fin.csv', 'rU' )  
reader = csv.DictReader(filefinal, fieldnames = ("code","name","priceUSD","priceReal","change24H", "symbol", "priceBTC", "volume24H", "timestamp" ))