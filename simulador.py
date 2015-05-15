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


def rodar_simulador():
	## inicializar lista de eventos
	# fila de eventos
	global eventos
	eventos.append(gerar_evento())

	## tratar eventos

	while eventos:
		trata_evento(eventos.popleft())

	print "tempo de leilao: {0}".format(tempo_leilao)


def gerar_evento():
	# considerando variáveis aleatórias com distribuição exponencial
	prob_termino_turno = taxa_turno_leilao / float(taxa_turno_leilao + taxa_apostas)
	u = random()
	if (u < prob_termino_turno):
		# tempo de termino de turno foi menor
		amostra = gera_amostra(taxa_turno_leilao)
		evento = 1 # fim do turno
	else:
		# tempo de chegada de aposta foi menor
		amostra = gera_amostra(taxa_apostas)
		evento = 2 # chegada de aposta
	return [evento, amostra]

def gera_amostra(taxa):
	# gerador de amostras com distribuição exponencial
	u = random()
	return (-1) * log(1 - u) / taxa

def trata_evento(evento):
	# anotar evento
	global f
	global tempo_leilao
	tempo_leilao += evento[1]
	if evento[0] == 1:
		f.write("{0},{1}\n".format("termino_turno", evento[1]))
		trata_termino_turno()
	if evento[0] == 2:
		f.write("{0},{1}\n".format("chegada_aposta", evento[1]))
		trata_chegada_aposta()

def trata_chegada_aposta():
	global valor_item
	valor_item += valor_aposta
	# define próximo evento
	global eventos
	eventos.append(gerar_evento())

def trata_termino_turno():
	# no caso de leilão com reset de apostas
	pass

for x in xrange(1,10):
	rodar_simulador()

f.close()
