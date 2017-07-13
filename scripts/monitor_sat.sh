#! /bin/bash

NAME="monitor_sat"

echo "Starting $NAME"
cd /webapps/satconnect/src/
exec  /webapps/smartcfdi/envlnx/bin/python monitor_sat.py
