# -*- coding: utf-8 -*-


#Práctica 1 de Computación en Red
#Máster Universitario de Ingeniería de Telecomunicaciones
#Realizado por Manuel Soler Borrego: manuel.soler@edu.uah.es


from flask import Flask,render_template, request, redirect
import funciones as f
import sys

app = Flask(__name__)
text = ""


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		umbral = request.form['umbral']
		#Comprobamos si es correcto el valor introducido:
		if umbral.isdigit():
			umbral = float(umbral)
			if 0<=umbral:
				print umbral
				text_u = 'Se ha establecido el umbral en %d' % (umbral) #umbralfunc(umbral)
				#print text
				text = f.formateardatos(umbral)
				return render_template("index.html", filas = text, variable = text_u)
			else:
				text_u = 'ERROR: El umbral debe ser mayor de cero.'
		else:
			text_u = 'ERROR: El umbral debe ser un numero entero positivo.'
		text = f.formateardatos()
		return render_template("index.html", filas = text, variable = text_u)
	if request.method == 'GET':
		text = f.formateardatos()
		return render_template("index.html", filas = text )
		
@app.route('/media')
def calcularmedia():
	media = f.media()
	text = f.formateardatos()
	return render_template("index.html", filas=text, media = media )

	
@app.route('/graficas')	
def graficas():
	return render_template("graficas.html" )

if __name__ == '__main__':
	print 'Se ha iniciado la aplicacion.'
	app.debug = True
	app.run(host ='0.0.0.0', port=80)
	f.init()
	

