#!/bin/bash
echo Iniciando servicio de Base de datos

sudo service mongod start

echo Servicio Mongod inicializado

echo Iniciando DuckDNS

su - ubuntu -c "nohup ~/Scripts/duck.sh > ~/Scripts/duck.log 2>&1&"

echo Entrando en entorno virtual

. /home/ubuntu/compu2018/flask/bin/activate

echo Iniciando aplicacion

sudo su

python /home/ubuntu/compu2018/app.py &


