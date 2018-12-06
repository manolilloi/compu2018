# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 20:36:36 2018

@author: Manu
"""
import urllib
import ssl
import re
import threading
from datetime import datetime, time, date
import pymongo
import numpy as np
from beebotte import *
import sys

_accesskey  = 'ecccee08185ec07b98aa16c40d4d9d26'
_secretkey  = '98819c9232d8bcb205c9142b2e02d9c0b907596f32ec0440e18d76685cc76ef5'
bclient = BBT( _accesskey, _secretkey)
con = pymongo.MongoClient()
db = con.localdb
entradas = db.entradas
alt = 0
#############################################
gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
# Opcional. Se puede usar si la web no acepta
#peticiones.
#############################################
def init():
	extraerinfo()

def consultarweb():
	url = 'http://www.meneame.net'
	texto = urllib.urlopen(url, context = gcontext).read()
	titular = re.search('<a\s*href=".*?"\s*class="l:\d*"\s*>(.*?)<\/a>',texto).group(1)
	print titular
	meneos = int(re.search('(\d+)<\/a>\s*meneos' ,texto).group(1))
	print "Meneos = %d" % (meneos)
	clics = int(re.search('(\d+)\s*clics' ,texto).group(1))
	print "Clics = %d" % (clics)
	hoy = datetime.today()
	tiempo = hoy.strftime("%Y/%m/%d %H:%M:%S")
	print tiempo
	return titular,meneos,clics,tiempo
	
def extraerinfo():
	titular,meneos,clics,tiempo = consultarweb()
	entradadb = {'Titular' : titular, 'Meneos' : meneos, 'Clics' : clics, 'Timestamp' : tiempo }
	entradas.insert(entradadb)
	bclient.write('compu2018', 'titular', titular)
	bclient.write('compu2018', 'meneos', meneos)
	bclient.write('compu2018', 'clics', clics)
	t = threading.Timer(120.0, extraerinfo)
	t.start()
  
def media():
	clics = []
	global alt
	if alt == 0 :
		ddbb = ' (Local)'
		lista_clics = entradas.find().sort('Clics')
		for entry in lista_clics:
			clics.append(entry['Clics'])
		alt = ~alt
	else :	
		ddbb = ' (Externa)'
		lista_clics = bclient.read('compu2018', 'clics', limit = 750)
		for entry in lista_clics:
			clics.append(entry['data'])
		alt = ~alt
	mean = np.mean(clics)
	 
	return float("{0:.2f}".format(mean)), ddbb
  
def formateardatos(th = None):
	if th == None :
		titular,meneos,clics,tiempo = consultarweb()
		# lista = entradas.find().sort('Timestamp', pymongo.DESCENDING)
		# for entry in lista:
			# titular = entry['Titular']
			# meneos = str(entry['Meneos'])
			# clics = str(entry['Clics'])
			# timestamp = entry['Timestamp']
		text = '<tr><td>'+titular+'</td> <td>'+str(meneos)+'</td><td>'+str(clics)+'</td><td>'+str(tiempo)+'</td></tr>'
		return text
	else :
		text = ""
		titular_anterior=""
		lista = entradas.find().sort('Timestamp', pymongo.DESCENDING)
		contador = 0
		for entry in lista:
			titular = entry['Titular']
			if entry['Clics'] > th and titular_anterior!=titular:
				contador = contador + 1
				if contador > 10 :
					break
				meneos = str(entry['Meneos'])
				clics = str(entry['Clics'])
				timestamp = str(entry['Timestamp'])
				text = text + '<tr><td>'+titular+'</td> <td>'+meneos+'</td><td>'+clics+'</td><td>'+timestamp+'</td></tr>'
				titular_anterior = titular
		return text
	
	
	
	
	