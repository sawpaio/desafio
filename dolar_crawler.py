import requests
import csv
import os
from datetime import datetime
import time

## Faz a Leitura da Página em HTML
def leiturapagina():
	requi = requests.get(url="https://m.investing.com/currencies/usd-brl", headers={'User-Agent':'curl/7.52.1'})
	verifica(requi) ## Passa o HTML
	formatadata(requi.headers["Date"])
#	print(requi.text)
#	formatadata(requi)

## Verifica se a requisição da página foi coletada.
def verifica(requi):
	if(requi.status_code == 200):
		print("A requisição foi feita com sucesso.")
		txt(requi)
	else:
		print("A requisição falhou")

def txt(requi):
	lista = requi.text
	escreve(formatacao(moeda(lista),cotacao(lista),percentual(lista),mudanca(lista),formatadata(requi.headers["Date"])))

#Função para procurar as frases próximas ao desejado.
def procurateste(texto):
	posicao = texto.find("data-date-created")
	if posicao >= 0:
		print("Encontrou na posição %d" %posicao)
		#print(texto[18586:18591])

def moeda(lista):
	valormoeda = lista.find("instrumentH1inlineblock")+30
#	print(valormoeda)
	return (lista[valormoeda:valormoeda+31])

def cotacao(lista):
	valoratual = lista.find("lastInst pid-2103-last")+30
#	print(valoratual)
	return (lista[valoratual:valoratual+18])

def mudanca(lista):
	valormudanca = lista.find("pid-2103-pc") + 35
#	print(valormudanca)
	return (lista[valormudanca:valormudanca+20])

def percentual(lista):
	valorpercentual = lista.find("pid-2103-pcp") + 35
#	print(valorpercentual)
	return (lista[valorpercentual:valorpercentual+8])

def formatadata(data):
	#print (time)
	now = datetime.now()
	datapronta = datetime.timestamp(now)
	return datapronta

def formatacao(valormoeda,valoratual,valormudanca,valorpercentual,datapronta):
	lista2 = [valormoeda,valoratual,valormudanca,valorpercentual,datapronta]
	return lista2

#Escreve o CSV, no formato solicitado.
def escreve(lista2):
	file = open("/lucasSampaio/crawler_dolar/dolar_data.csv", 'a+')
	wr = csv.writer(file)
	filesize = os.stat("/lucasSampaio/crawler_dolar/dolar_data.csv").st_size
	if filesize == 0:
		wr.writerow(['currency', 'value', 'change','perc', 'timestamp'])
	wr.writerow(lista2)

def main():
	leiturapagina()
	#print("Cotação atualizada.")

main()

