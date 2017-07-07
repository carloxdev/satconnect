# -*- coding: utf-8 -*-

from LibTools.filesystem import Carpeta
from slaves import SentinelCxp

if __name__ == '__main__':

    carpeta = Carpeta(
        '/Users/Carlos/Files/Trabajo/Sintaxys/Proyectos/SatConnect/comprobantes/monitor_cxp'
    )
    sentinela = SentinelCxp(carpeta)
    sentinela.start_Monitoring()
