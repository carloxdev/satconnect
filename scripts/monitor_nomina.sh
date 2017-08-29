#! /bin/bash

NAME="monitor_nomina"

echo "Starting $NAME"
cd /webapps/satconnect/src/
exec  /webapps/smartcfdi/envlnx/bin/python monitor_nomina.py
