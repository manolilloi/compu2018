#!/bin/bash

echo Iniciando servicio de Base de datos

service mongod start

echo Servicio Mongod inicializado

echo Entrando en entorno virtual

. /home/ubuntu/compu2018/flask/bin/activate

echo Iniciando aplicacion

python /home/ubuntu/compu2018/app.py &
