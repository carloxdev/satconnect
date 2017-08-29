# -*- coding: utf-8 -*-
from LibTools.filesystem import Carpeta
from slaves import SentinelNomina

import settings

if __name__ == '__main__':

    carpeta = Carpeta(settings.folder_nomina)
    sentinela = SentinelNomina(carpeta)
    sentinela.start_Monitoring()
