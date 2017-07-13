#! /bin/bash

NAME="monitor_cxp"

echo "Starting $NAME"
cd /webapps/satconnect/src/
exec  /webapps/smartcfdi/envlnx/bin/python monitor_cxp.py
