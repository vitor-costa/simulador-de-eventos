#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import deque
from math import log
from random import *

f = open('eventos.txt', 'w')

# inicializar variáveis de estado
valor_item = 0
valor_aposta = 1
taxa_turno_leilao = 1
taxa_apostas = 2
tempo_leilao = 0
eventos = deque([])

# variaveis problema
elementos_na_fila = 0
tempo = 0
servidor_ocupado = False

uniforme = 0
tipo = "poisson"


def rodar_simulador():
	## inicializar lista de eventos
	# fila de eventos
	global eventos
	eventos.append(gerar_evento())

	## tratar eventos

	count = 1
	while eventos and count <= 100:
		trata_evento(eventos.popleft())
		count += 1

	print "tempo: {0}".format(tempo)


# def gerar_evento():
# 	# considerando variáveis aleatórias com distribuição exponencial
# 	prob_termino_turno = taxa_turno_leilao / float(taxa_turno_leilao + taxa_apostas)
# 	u = random()
# 	if (u < prob_termino_turno):
# 		# tempo de termino de turno foi menor
# 		amostra = gera_amostra(taxa_turno_leilao)
# 		evento = 1 # fim do turno
# 	else:
# 		# tempo de chegada de aposta foi menor
# 		amostra = gera_amostra(taxa_apostas)
# 		evento = 2 # chegada de aposta
# 	return [evento, amostra]

def gerar_evento():
	soma_taxas = 1
	# considerando variáveis aleatórias com distribuição exponencial
	prob_chegada = taxa_chegada / float(soma_taxas)
	prob_saida = taxa_saida / float(soma_taxas)
	prob_reentrada = taxa_reentrada / float(soma_taxas)
	u = random()
	if u < prob_chegada:
		# gera chegada
		amostra = gera_amostra_chegada(taxa_chegada)
		evento = 1
	elif u < prob_chegada + prob_saida:
		# gera saida
		amostra = gera_amostra(taxa_saida)
		evento = 2
	else:
		# gera reentrada
		amostra = gera_amostra(taxa_reentrada)
		evento = 3
	return [evento, amostra]

def gera_amostra_chegada(taxa):
	# gerador de amostras com distribuição exponencial
	global tipo
	u = random()
	if tipo == "poisson":
		return (-1) * log(1 - u) / taxa
	if tipo == "deterministico":
		return taxa
	if tipo == "uniforme":
		if uniforme == 0:
			return int((u * 10) + 5)
		else:
			return int((u * 100) + 50)

def gera_amostra(taxa):
	# gerador de amostras com distribuição exponencial
	u = random()
	return (-1) * log(1 - u) / taxa

# def trata_evento(evento):
# 	# anotar evento
# 	global f
# 	global tempo_leilao
# 	tempo_leilao += evento[1]
# 	if evento[0] == 1:
# 		f.write("{0},{1}\n".format("termino_turno", evento[1]))
# 		trata_termino_turno()
# 	if evento[0] == 2:
# 		f.write("{0},{1}\n".format("chegada_aposta", evento[1]))
# 		trata_chegada_aposta()

def trata_evento(evento):
	# anotar evento
	global f
	global tempo
	tempo += evento[1]
	if evento[0] == 1:
		f.write("{0},{1},{2}\n".format("chegada", evento[1], elementos_na_fila))
		trata_chegada()
	if evento[0] == 2:
		f.write("{0},{1},{2}\n".format("saida", evento[1], elementos_na_fila))
		trata_saida()
	if evento[0] == 3:
		f.write("{0},{1},{2}\n".format("reentrada", evento[1], elementos_na_fila))
		trata_reentrada()

def trata_chegada():
	global eventos
	global elementos_na_fila
	global servidor_ocupado
	
	elementos_na_fila += 1
	if not servidor_ocupado:
		servidor_ocupado = True
	eventos.append(gerar_evento())

def trata_saida():
	global eventos
	global elementos_na_fila
	global servidor_ocupado

	if elementos_na_fila > 0:
		elementos_na_fila -= 1
	elif servidor_ocupado:
		servidor_ocupado = False
	eventos.append(gerar_evento())

def trata_reentrada():
	global eventos
	global elementos_na_fila
	global servidor_ocupado

	if servidor_ocupado:
		elementos_na_fila += 1
	eventos.append(gerar_evento())

# def trata_chegada_aposta():
# 	global valor_item
# 	valor_item += valor_aposta
# 	# define próximo evento
# 	global eventos
# 	eventos.append(gerar_evento())

# def trata_termino_turno():
# 	# no caso de leilão com reset de apostas
# 	pass

# for x in xrange(1,2):
# 	rodar_simulador()

# cenario 1
taxa_chegada = 0.05
taxa_saida = 1
taxa_reentrada = 0
while taxa_chegada<=0.9:
	rodar_simulador()
	taxa_chegada += 0.05
	f.write("=" * 50)
	f.write("\n")

# cenario 2
taxa_chegada = 0.05
taxa_saida = 1
taxa_reentrada = 0
tipo = "deterministico"
while taxa_chegada<=0.9:
	rodar_simulador()
	taxa_chegada += 0.05
	f.write("=" * 50)
	f.write("\n")

# cenario 3
taxa_chegada = 0.1
taxa_saida = 1
taxa_reentrada = 1
tipo = "uniforme"
while taxa_saida<=10:
	rodar_simulador()
	taxa_saida += 0.5
	f.write("=" * 50)
	f.write("\n")

# cenario 4
taxa_chegada = 0.01
taxa_saida = 1
taxa_reentrada = taxa_chegada * 0.9
tipo = "poisson"
while taxa_saida<=10:
	rodar_simulador()
	taxa_saida += 0.5
	f.write("=" * 50)
	f.write("\n")

# cenario 5
taxa_chegada = 0.01
taxa_saida = 1
taxa_reentrada = taxa_chegada * 0.9
tipo = "deterministico"
while taxa_saida<=10:
	rodar_simulador()
	taxa_saida += 0.5
	f.write("=" * 50)
	f.write("\n")

# cenario 6
taxa_chegada = 0.01
taxa_saida = 1
taxa_reentrada = taxa_chegada * 0.9
tipo = "uniforme"
while taxa_saida<=10:
	rodar_simulador()
	taxa_saida += 0.5
	f.write("=" * 50)
	f.write("\n")

f.close()
