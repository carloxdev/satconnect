# -*- coding: utf-8 -*-
from LibTools.filesystem import Carpeta
from slaves import SentinelSat

import settings

if __name__ == '__main__':

    carpeta = Carpeta(settings.folder_sat)
    sentinela = SentinelSat(carpeta)
    sentinela.start_Monitoring()
