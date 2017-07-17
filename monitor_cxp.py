# -*- coding: utf-8 -*-
from LibTools.filesystem import Carpeta
from slaves import SentinelCxp

import settings

if __name__ == '__main__':

    carpeta = Carpeta(settings.folder_cxp)
    sentinela = SentinelCxp(carpeta)
    sentinela.start_Monitoring()
