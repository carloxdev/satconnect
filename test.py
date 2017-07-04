# -*- coding: utf-8 -*-

from LibTools.filesystem import Archivo
from LibTools.filesystem import Carpeta
from LibTools.data import Escriba
from LibTools.data import Error
# from documentos import Log
# import logging

try:

    folder_log = Carpeta('/Users/Carlos/Files/Trabajo/Sintaxys/Proyectos/SatConnect/media/monitor_cxp/logs')
    log_file = Archivo(folder_log, "mi_log.txt")

    escriba = Escriba(log_file)
    escriba.set_show_InConsole()
    escriba.set_save_InFile()

    log = escriba.get_Log()
    # logger = logging.getLogger('satconnector')
    # logger.setLevel(logging.INFO)

    # hdlr = logging.FileHandler('/Users/Carlos/Files/Trabajo/Sintaxys/Proyectos/SatConnect/pruebas/super.log')
    # formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    # hdlr.setFormatter(formatter)
    # logger.addHandler(hdlr)

    # # log.capturar_Texto()
    # import ipdb; ipdb.set_trace()
    log.error('cdc')
    log.info('carlós')

    # log.terminar_Captura()


except Error as error:
    print error
