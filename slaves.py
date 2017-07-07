# -*- coding: utf-8 -*-

# Python's Libaries
import os
import time
from datetime import datetime

# Own's Libraries
from LibTools.filesystem import Carpeta
from LibTools.filesystem import Archivo
from LibTools.data import Error
from LibTools.memory import LogMemory
from LibTools.communication import Postman

from sat import WebServiceSAT

from documents import Comprobante

from smartsite import ModeloEmpresa
from smartsite import ModeloComprobanteProveedor
from smartsite import ModeloEmailAccount
from smartsite import ModeloF0101
from smartsite import ModeloF5903000


class Sentinel(object):

    def __init__(self, _folder):

        self.folder = _folder

        self.folder_pendientes = Carpeta(
            os.path.join(
                self.folder.abspath,
                'pendientes'
            )
        )

        self.folder_procesadas = Carpeta(
            os.path.join(
                self.folder.abspath,
                'procesadas'
            )
        )

        self.folder_no_procesadas = Carpeta(
            os.path.join(
                self.folder.abspath,
                'no_procesadas'
            )
        )

        self.folder_no_empresa = Carpeta(
            os.path.join(
                self.folder.abspath,
                'no_empresa'
            )
        )

        self.folder_no_encontradas_sat = Carpeta(
            os.path.join(
                self.folder.abspath,
                'no_encontradas_sat'
            )
        )

        self.log = LogMemory()

    def move_To_NoProcesadas(self, _file, _with_pdf=False):

        _file.move(self.folder_no_procesadas, _replace=True)
        self.log.line("Mover archivo %s.......OK" % (_file.nombre))

        if _with_pdf:

            try:
                filePdf_name = _file.nombre.replace(
                    'xml',
                    'pdf'
                ).replace(
                    'XML',
                    'PDF'
                )
                filePdf = Archivo(self.folder_pendientes, filePdf_name)
                filePdf.move(self.folder_no_procesadas, _replace=True)
                self.log.line("Mover archivo %s.......OK" % (filePdf.nombre))

            except Exception as error:
                self.log.line(error)

    def move_To_NoEmpresa(self, _file, _with_pdf=False):

        _file.move(self.folder_no_empresa, _replace=True)
        self.log.line("Mover archivo %s.......OK" % (_file.nombre))

        if _with_pdf:

            try:

                filePdf_name = _file.nombre.replace(
                    'xml',
                    'pdf'
                ).replace(
                    'XML',
                    'PDF'
                )
                filePdf = Archivo(self.folder_pendientes, filePdf_name)
                filePdf.move(self.folder_no_empresa, _replace=True)
                self.log.line("Mover archivo %s.......OK" % (filePdf.nombre))

            except Exception as error:
                self.log.line(error)

    def move_To_NoEncontradasSAT(self, _file, _with_pdf=False):

        _file.move(self.folder_no_encontradas_sat, _replace=True)
        self.log.line("Mover archivo %s.......OK" % (_file.nombre))

        if _with_pdf:
            try:

                filePdf_name = _file.nombre.replace(
                    'xml',
                    'pdf'
                ).replace(
                    'XML',
                    'PDF'
                )
                filePdf = Archivo(self.folder_pendientes, filePdf_name)
                filePdf.move(self.folder_no_encontradas_sat, _replace=True)
                self.log.line("Mover archivo %s.......OK" % (filePdf.nombre))

            except Exception as error:
                self.log.line(error)

    def move_To_Procesadas(self, _file, _folder, _with_pdf=False):

        _file.move(_folder, _replace=True)
        self.log.line("Mover archivo %s.......OK" % (_file.nombre))

        if _with_pdf:

            try:

                filePdf_name = _file.nombre.replace(
                    'xml',
                    'pdf'
                ).replace(
                    'XML',
                    'PDF'
                )
                filePdf = Archivo(self.folder_pendientes, filePdf_name)
                filePdf.move(_folder, _replace=True)
                self.log.line("Mover archivo %s.......OK" % (filePdf_name))

            except Exception as error:
                self.log.line(error)

    def create_Folder_Validas(self, _file):

        origin = "Sentinel.create_Folder_Validas()"

        new_folders = [
            "procesadas",
            _file.empresa_clave,
            _file.fecha.strftime('%Y'),
            _file.fecha.strftime('%m'),
            "validas",
            _file.emisor_rfc
        ]

        abspath_validas = os.path.join(
            self.folder.abspath,
            *new_folders
        )

        folder_validas = Carpeta(abspath_validas)

        try:

            self.folder.add_Folders(new_folders)

            folder_validas.exist(origin)

            self.log.line("Creacion de folder VALIDAS (CXP).......OK")

            return folder_validas

        except Exception as error:

            if error.control == "carpeta ya existe":

                self.log.line("Creacion de folder VALIDAS (CXP).......Carpeta ya existe")
                return folder_validas

            else:
                self.log.line("Creacion de folder VALIDAS (CXP).......%s" % (str(error)))
                self.log.line("No se logro crear el folder de VALIDAS(CXP), por lo que se movera a NO_PROCESADAS")
                self.move_To_NoProcesadas(_file, _with_pdf=True)

                raise Error(
                    "validacion",
                    origin,
                    "error al crear carpeta validas",
                    str(error)
                )

    def create_Folder_NoValidas(self, _file):

        origin = "Sentinel.create_Folder_NoValidas()"

        new_folders = [
            "procesadas",
            _file.empresa_clave,
            _file.fecha.strftime('%Y'),
            _file.fecha.strftime('%m'),
            "no_validas",
            _file.emisor_rfc
        ]

        abspath_novalidas = os.path.join(
            self.folder.abspath,
            *new_folders
        )

        folder_novalidas = Carpeta(abspath_novalidas)

        try:

            self.folder.add_Folders(new_folders)

            folder_novalidas.exist(origin)

            self.log.line("Creacion de folder NO_VALIDAS (CXP).......OK")

            return folder_novalidas

        except Exception as error:

            if error.control == "carpeta ya existe":

                self.log.line("Creacion de folder NO_VALIDAS (CXP).......Carpeta ya existe")
                return folder_novalidas

            else:
                self.log.line("Creacion de folder NO_VALIDAS (CXP).......%s" % (str(error)))
                self.log.line("No se logro crear el folder de NO_VALIDAS(CXP), por lo que se movera a NO_PROCESADAS")
                self.move_To_NoProcesadas(_file, _with_pdf=True)

                raise Error(
                    "validacion",
                    origin,
                    "error al crear carpeta no_validas",
                    str(error)
                )

    def validate_Extension(self, _file):

        origin = "Sentinel.validate_Extension()"

        if _file.extension == ".xml" or _file.extension == ".XML":
            self.log.line("Extension del archivo.......XML")

        elif _file.extension == ".pdf" or _file.extension == ".PDF":
            self.log.line("Extension del archivo.......PDF (Se movera junto con el archivo XML)")

            raise Error(
                "validacion",
                origin,
                "Extension PDF",
                "La extension es PDF"
            )

        else:
            self.log.line(
                "Archivo con extension no esperada.......%s. (Se movera a no procesados)" % (_file.extension)
            )

            self.move_To_NoProcesadas(_file, _with_pdf=False)

            raise Error(
                "validacion",
                origin,
                "extension desconocida",
                "La extension es Desconocida"
            )

    def read_File(self, _file):

        origin = "Sentinel.read_File()"

        _file.read()

        if _file.uuid != "":
            self.log.line(_file)

        else:
            self.log.line(
                "No se encontro UUID en el archivo XML, por lo cual se movera a NO_PROCESADAS"
            )

            self.move_To_NoProcesadas(_file, _with_pdf=True)

            raise Error(
                "validacion",
                origin,
                "no uuid",
                "El archivo no contiene UUID"
            )

    def validate_Empresa_InSmart(self, _file):

        origin = "Sentinel.validate_Empresa_InSmart()"

        try:
            empresa = ModeloEmpresa.get_ByRfc(_file.receptor_rfc)
            _file.empresa_clave = empresa.clave
            self.log.line("Validacion de empresa.......OK")

        except Exception as error:

            self.log.line("Validacion de empresa.......%s." % (error.mensaje))

            self.log.line("No se pudo validar la Empresa por lo cual se movera a NO_EMPRESA")

            self.move_To_NoEmpresa(_file, _with_pdf=True)

            raise Error(
                "validacion",
                origin,
                "no empresa",
                str(error)
            )

    def validate_Estado_InSat(self, _file):

        origin = "Sentinel.validate_Estado_InSat()"

        try:
            webservice = WebServiceSAT()
            estado_sat = webservice.get_Estado(
                _file.emisor_rfc,
                _file.receptor_rfc,
                _file.total,
                _file.uuid
            )

            _file.estadoSat = estado_sat.encode('utf-8')
            _file.fecha_validacion = datetime.now().date()

            self.log.line("Estado en SAT ......%s" % (estado_sat.encode('utf-8')))

        except Exception as error:

            self.log.line("Validar estado en SAT.......%s" % (str(error)))

            self.log.line("No se pudo validar el estado en el portal SAT, por lo cual se movera a NO_ENCONTRADAS_SAT")

            self.move_To_NoEncontradasSAT(_file, _with_pdf=True)

            raise Error(
                "validacion",
                origin,
                "error al obtener estado sat",
                str(error)
            )

    def report_Results(self, _title):

        try:

            self.log.section("INFORMANDO RESULTADOS")

            settings = ModeloEmailAccount.get_ByClave("notificaciones")
            cartero = Postman(
                settings.account,
                settings.password,
                settings.smtp_server,
                settings.people
            )

            cartero.send_Gmail_Message(_title, self.log.texto)

        except Exception as error:
            print str(error)


class SentinelSat(Sentinel):

    def change_Status_InSmart(self, _file):

        origin = "Sentinel.change_Status_InSmart()"

        try:
            ModeloComprobanteProveedor.update_SatStatus(_file)
            self.log.line("Cambiar Estado SAT en SmartCFDI......OK")

        except Exception as error:
            self.log.line("Cambiar Estado SAT en SmartCFDI.......%s" % (error.mensaje))

            self.log.line("No se pudo actualizar el Estado SAT en SmartCFDI por lo cual se movera a NO_PROCESADAS")

            self.move_To_NoProcesadas(_file, _with_pdf=True)

            raise Error(
                "validacion",
                origin,
                "error al actualizar estado in smart",
                str(error)
            )

    def save_InSmart(self, _file):

        origin = "Sentinel.save_InSmart()"

        try:
            ModeloComprobanteProveedor.add(_file)
            self.log.line("Guardar en SmartCFDI.......OK")

        except Exception as error:

            if error.control == "registro ya existe":
                self.log.line("Guardar en SmartCFDI.......Ya existe en BD")

            else:
                self.log.line("Guardar en SmartCFDI.......%s" % (error.mensaje))

                self.log.line("No se pudo guardar en SmartCFDI por lo cual se movera a NO_PROCESADAS")

                self.move_To_NoProcesadas(_file, _with_pdf=True)

                raise Error(
                    "validacion",
                    origin,
                    "error al guardar in smart",
                    str(error)
                )

    def start_Monitoring(self):

        self.log.section(
            "COMENZANDO MONITORIO DE CARPETA: %s" % (self.folder_pendientes.abspath)
        )

        before = dict([(f, None) for f in os.listdir(self.folder_pendientes.abspath)])

        while 1:
            time.sleep(10)
            after = dict([(f, None) for f in os.listdir(self.folder_pendientes.abspath)])
            added = [f for f in after if not f in before]
            removed = [f for f in before if not f in after]

            if added:
                self.process_Files(added)

            if removed:
                # elSentinela.toProcessInvoices(removed)
                print "\nRemoved: ", ", ".join(removed)
                # Aqui va ir el codigo que revisa

            before = after

    def process_Files(self, _file_names):

        self.log.section(
            "ARCHIVOS DEL SAT A CARGAR: %s" % (len(_file_names))
        )

        count_procesados = 0

        for filename in _file_names:

            try:
                count_procesados += 1

                self.log.section(
                    "PORCESANDO ARCHIVO %s DE %s: %s" % (
                        count_procesados,
                        len(_file_names),
                        filename
                    )
                )

                file = Comprobante(
                    self.folder_pendientes,
                    filename
                )

                self.validate_Extension(file)

                self.read_File(file)

                self.validate_Empresa_InSmart(file)

                self.save_InSmart(file)

                self.validate_Estado_InSat(file)

                if file.estadoSat == "Vigente":

                    self.log.line("Comprobante con estado Valido se movera a VALIDAS")

                    self.change_Status_InSmart(file)

                    folder_validas = self.create_Folder_Validas(file)

                    self.move_To_Procesadas(file, folder_validas, _with_pdf=False)

                elif file.estadoSat == "Cancelado":

                    self.log.line("Comprobante con estado Cancelado se movera a NO_VALIDAS")

                    self.change_Status_InSmart(file)

                    folder_novalidas = self.create_Folder_NoValidas(file)

                    self.move_To_Procesadas(file, folder_novalidas, _with_pdf=False)

                elif file.estadoSat == 'No Encontrado':

                    self.change_Status_InSmart(file)

                    self.log.line("Comprobante con estado No Encontrado se movera a NO_ENCONTRADAS_SAT")

                    self.move_To_NoEncontradasSAT(file, _with_pdf=False)

                else:
                    self.change_Status_InSmart(file)

                    self.log.line("Comprobante con estado DESCONOCIDO se movera a NO_PROCESADAS")

                    self.move_To_NoProcesadas(file, _with_pdf=False)

            except Exception, error:

                if error.__class__.__name__ == "Error":
                    if error.control == "xml corrupto":

                        self.log.line("El archivo tiene un formato XML incorrecto, se movera a NO_PROCESADAS")

                        file = Archivo(
                            self.folder_pendientes,
                            filename
                        )

                        self.move_To_NoProcesadas(file, _with_pdf=True)

                else:
                    print str(error)

        self.report_Results("Carga de comprobantes SAT")


class SentinelCxp(SentinelSat):

    def validate_Proveedor_InJDE(self, _file):

        origin = "Sentinel.validate_Proveedor_InJDE()"

        try:
            proveedor = ModeloF0101.get_ByRfc(_file.emisor_rfc)
            _file.emisor_jde_clave = proveedor.clave
            self.log.line("Validacion de Proveedor.......OK")

        except Exception as error:

            self.log.line("Validacion de Proveedor.......%s." % (error))

            self.log.line("Ocurrio error al validar Proveedor, por lo cual se movera a NO_PROCESADOS")

            self.move_To_NoProcesadas(_file, _with_pdf=True)

            raise Error(
                "validacion",
                origin,
                "no proveedor",
                str(error)
            )

    def validate_Exist_InSmart(self, _file):

        origin = "Sentinel.validate_Exist_InSmart()"

        try:
            comprobante = ModeloComprobanteProveedor.get(_file.uuid)
            self.log.line("Validacion de Comprobante.......OK")

        except Exception as error:

            self.log.line("Validacion de Comprobante.......%s." % (error.mensaje))

            self.log.line("No se pudo encontrar el Comprobante por lo cual se movera a NO_PROCESADOS")

            self.move_To_NoProcesadas(_file, _with_pdf=True)

            raise Error(
                "validacion",
                origin,
                "no comprobante",
                str(error)
            )

    def save_InJDE(self, _file):

        origin = "Sentinel.save_InJDE()"

        try:
            ModeloF5903000.add(_file)
            self.log.line("Guardar en JDE.......OK")

        except Exception as error:

            if error.control == "registro ya existe":
                self.log.line("Guardar en JDE.......Ya existe en BD")

            else:
                self.log.line("Guardar en JDE.......%s" % (error.mensaje))

                self.log.line("No se pudo guardar en JDE por lo cual se movera a NO_PROCESADAS")

                self.move_To_NoProcesadas(_file, _with_pdf=True)

                raise Error(
                    "validacion",
                    origin,
                    "error al guardar in smart",
                    str(error)
                )

    def mark_Reception_InSmart(self, _file):

        origin = "Sentinel.mark_Reception_InSmart()"

        try:
            _file.comprobacion = "REC"
            ModeloComprobanteProveedor.update_Comprobacion(_file)
            self.log.line("Marcar de recibido en SmartCFDI......OK")

        except Exception as error:
            self.log.line("Marcar de recibido en SmartCFDI.......%s" % (error.mensaje))

            self.log.line("No se pudo marcar de recibido en SmartCFDI por lo cual se movera a NO_PROCESADAS")

            self.move_To_NoProcesadas(_file, _with_pdf=True)

            raise Error(
                "validacion",
                origin,
                "error al marcar de recibido in smart",
                str(error)
            )

    def process_Files(self, _file_names):

        self.log.section(
            "ARCHIVOS DE CXP A PROCESAR: %s" % (len(_file_names))
        )

        count_procesados = 0

        for filename in _file_names:

            try:
                count_procesados += 1

                self.log.section(
                    "PORCESANDO ARCHIVO %s DE %s: %s" % (
                        count_procesados,
                        len(_file_names),
                        filename
                    )
                )

                file = Comprobante(
                    self.folder_pendientes,
                    filename
                )

                self.validate_Extension(file)

                self.read_File(file)

                self.validate_Empresa_InSmart(file)

                # self.save_InSmart(file)

                self.validate_Exist_InSmart(file)

                self.validate_Estado_InSat(file)

                if file.estadoSat == "Vigente":

                    self.log.line("Comprobante con estado Valido se movera a VALIDAS")

                    self.change_Status_InSmart(file)

                    self.mark_Reception_InSmart(file)

                    self.validate_Proveedor_InJDE(file)

                    self.save_InJDE(file)

                    folder_validas = self.create_Folder_Validas(file)

                    self.move_To_Procesadas(file, folder_validas, _with_pdf=True)

                elif file.estadoSat == "Cancelado":

                    self.log.line("Comprobante con estado Cancelado se movera a NO_VALIDAS")

                    self.change_Status_InSmart(file)

                    self.mark_Reception_InSmart(file)

                    folder_novalidas = self.create_Folder_NoValidas(file)

                    self.move_To_Procesadas(file, folder_novalidas, _with_pdf=True)

                elif file.estadoSat == 'No Encontrado':

                    self.change_Status_InSmart(file)

                    self.log.line("Comprobante con estado No Encontrado se movera a NO_ENCONTRADAS_SAT")

                    self.move_To_NoEncontradasSAT(file, _with_pdf=True)

                else:
                    self.change_Status_InSmart(file)

                    self.log.line("Comprobante con estado DESCONOCIDO se movera a NO_PROCESADAS")

                    self.move_To_NoProcesadas(file, _with_pdf=True)

            except Exception, error:

                if error.__class__.__name__ == "Error":
                    if error.control == "xml corrupto":

                        self.log.line("El archivo tiene un formato XML incorrecto, se movera a NO_PROCESADAS")

                        file = Archivo(
                            self.folder_pendientes,
                            filename
                        )

                        self.move_To_NoProcesadas(file, _with_pdf=True)

                else:
                    print str(error)

        self.report_Results("Revision de Facturas CXP")
