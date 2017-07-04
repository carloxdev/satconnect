# -*- coding: utf-8 -*-

from LibTools.filesystem import Carpeta
from slaves import Sentinel

if __name__ == '__main__':

    carpeta = Carpeta(
        '/Users/Carlos/Files/Trabajo/Sintaxys/Proyectos/SatConnect/media/monitor_cxp'
    )
    sentinela = Sentinel(carpeta)
    sentinela.start_Monitoring()
