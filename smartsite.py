# -*- coding: utf-8 -*-

# Python's Libraries
import os
import sys
import json
from datetime import datetime

import settings

sys.path.append(settings.project_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SmartCFDI.settings")


# Django's Libraries
from django.db import connection
from django.core.wsgi import get_wsgi_application
from django.core.files import File

application = get_wsgi_application()

# Site's Models
from configuracion.models import Empresa
from configuracion.models import EmailAccount
from facturas.models import ComprobanteProveedor
from facturas.models import ComprobanteEmpleado
from jde.models import F0101
from jde.models import F5903000

# Own's Libraries
from LibTools.data import Error
from LibTools.data import Validator


class ModeloEmpresa(object):

    @classmethod
    def get_ByRfc(self, _rfc):

        origin = "ModeloEmpresa.get_ByRfc()"

        try:
            connection.close()
            empresa = Empresa.objects.get(rfc=_rfc, activa=True)
            return empresa

        except Exception as error:

            if type(error).__name__ == 'DoesNotExist':
                raise Error(
                    "validacion",
                    origin,
                    "no empresa",
                    "No se encontro empresa"
                )

            else:
                raise Error(
                    type(error).__name__,
                    origin,
                    "",
                    str(error)
                )


class ModeloComprobanteProveedor(object):

    @classmethod
    def add(self, _comprobante):

        origin = "ModeloComprobanteProveedor.add()"

        try:
            connection.close()
            comprobante = ComprobanteProveedor(
                serie=_comprobante.serie,
                folio=_comprobante.folio,
                fecha=_comprobante.fecha,
                formaDePago=_comprobante.formaDePago,
                noCertificado=_comprobante.noCertificado,
                subTotal=_comprobante.subTotal,
                tipoCambio=_comprobante.tipoCambio,
                moneda=_comprobante.moneda,
                sello=_comprobante.sello,
                total=_comprobante.total,
                tipoDeComprobante=_comprobante.tipoDeComprobante,
                metodoDePago=_comprobante.metodoDePago,
                lugarExpedicion=_comprobante.lugarExpedicion,
                numCtaPago=_comprobante.numCtaPago,
                condicionesDePago=_comprobante.condicionesDePago,
                emisor_rfc=_comprobante.emisor_rfc,
                emisor_nombre=_comprobante.emisor_nombre,
                emisor_calle=_comprobante.emisor_calle,
                emisor_noExterior=_comprobante.emisor_noExterior,
                emisor_noInterior=_comprobante.emisor_noInterior,
                emisor_colonia=_comprobante.emisor_colonia,
                emisor_localidad=_comprobante.emisor_localidad,
                emisor_municipio=_comprobante.emisor_municipio,
                emisor_estado=_comprobante.emisor_estado,
                emisor_pais=_comprobante.emisor_pais,
                emisor_codigoPostal=_comprobante.emisor_codigoPostal,
                emisor_expedidoEn_calle=_comprobante.emisor_expedidoEn_calle,
                emisor_expedidoEn_noExterior=_comprobante.emisor_expedidoEn_noExterior,
                emisor_expedidoEn_noInterior=_comprobante.emisor_expedidoEn_noInterior,
                emisor_expedidoEn_colonia=_comprobante.emisor_expedidoEn_colonia,
                emisor_expedidoEn_municipio=_comprobante.emisor_expedidoEn_municipio,
                emisor_expedidoEn_estado=_comprobante.emisor_expedidoEn_estado,
                emisor_expedidoEn_pais=_comprobante.emisor_expedidoEn_pais,
                emisor_regimen=_comprobante.emisor_regimen,
                receptor_rfc=_comprobante.receptor_rfc,
                receptor_nombre=_comprobante.receptor_nombre,
                receptor_calle=_comprobante.receptor_calle,
                receptor_noExterior=_comprobante.receptor_noExterior,
                receptor_noInterior=_comprobante.receptor_noInterior,
                receptor_colonia=_comprobante.receptor_colonia,
                receptor_localidad=_comprobante.receptor_localidad,
                receptor_municipio=_comprobante.receptor_municipio,
                receptor_estado=_comprobante.receptor_estado,
                receptor_pais=_comprobante.receptor_pais,
                receptor_codigoPostal=_comprobante.receptor_codigoPostal,
                conceptos=json.dumps(_comprobante.conceptos),
                totalImpuestosTrasladados=_comprobante.totalImpuestosTrasladados,
                totalImpuestosRetenidos=_comprobante.totalImpuestosRetenidos,
                impuestos_trasladados=json.dumps(
                    _comprobante.impuestos_trasladados),
                impuestos_retenidos=json.dumps(
                    _comprobante.impuestos_retenidos),
                uuid=_comprobante.uuid,
                fechaTimbrado=_comprobante.fechaTimbrado,
                noCertificadoSAT=_comprobante.noCertificadoSAT,
                selloSAT=_comprobante.selloSAT
            )

            empresa = Empresa.objects.get(clave=_comprobante.empresa_clave)
            comprobante.empresa = empresa
            comprobante.save()

            comprobante.archivo_xml.save(_comprobante.nombre, File(open(_comprobante.get_Abspath(), 'r')))

            print "Se guardo el comprobante: {}".format(_comprobante.uuid)

        except Exception as error:

            if type(error).__name__ == "IntegrityError":

                raise Error(
                    "validacion",
                    origin,
                    "registro ya existe",
                    str(error)
                )

            else:
                raise Error(
                    type(error).__name__,
                    origin,
                    "",
                    str(error)
                )

    @classmethod
    def get(self, _uuid):

        origin = "ModeloComprobanteProveedor.get()"

        try:
            connection.close()
            factura = ComprobanteProveedor.objects.get(uuid=_uuid)
            return factura

        except Exception as error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    @classmethod
    def update_SatStatus(self, _comprobante):

        origin = "ModeloComprobanteProveedor.update_SatStatus()"

        try:
            connection.close()
            comprobante = ComprobanteProveedor.objects.get(uuid=_comprobante.uuid)
            comprobante.estadoSat = _comprobante.estadoSat
            comprobante.fecha_validacion = _comprobante.fecha_validacion
            comprobante.save()

            print "Se actualizo el comprobante: {}".format(_comprobante.uuid)

        except Exception as error:

            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    @classmethod
    def update_Comprobacion(self, _comprobante):

        origin = "ModeloComprobanteProveedor.update_Comprobacion()"

        try:
            connection.close()
            comprobante = ComprobanteProveedor.objects.get(uuid=_comprobante.uuid)
            comprobante.comprobacion = _comprobante.comprobacion

            file_name = _comprobante.nombre.replace(
                'xml',
                'pdf'
            ).replace(
                'XML',
                'PDF'
            )

            file_abspath = _comprobante.get_Abspath().replace(
                'xml',
                'pdf'
            ).replace(
                'XML',
                'PDF'
            )

            comprobante.archivo_pdf.save(file_name, File(open(file_abspath, 'r')))
            # comprobante.save()

            print "Se actualizo el comprobante: {}".format(_comprobante.uuid)

        except Exception as error:

            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    @classmethod
    def update(self, _comprobante):

        origin = "ModeloComprobanteProveedor.update()"

        try:
            connection.close()

            comprobante = ComprobanteProveedor.objects.get(uuid=_comprobante.uuid)
            comprobante.serie = _comprobante.serie
            comprobante.folio = _comprobante.folio
            comprobante.fecha = _comprobante.fecha
            comprobante.formaDePago = _comprobante.formaDePago
            comprobante.noCertificado = _comprobante.noCertificado
            comprobante.subTotal = _comprobante.subTotal
            comprobante.tipoCambio = _comprobante.tipoCambio
            comprobante.moneda = _comprobante.moneda
            comprobante.sello = _comprobante.sello
            comprobante.total = _comprobante.total
            comprobante.tipoDeComprobante = _comprobante.tipoDeComprobante
            comprobante.metodoDePago = _comprobante.metodoDePago
            comprobante.lugarExpedicion = _comprobante.lugarExpedicion
            comprobante.numCtaPago = _comprobante.numCtaPago
            comprobante.condicionesDePago = _comprobante.condicionesDePago
            comprobante.emisor_rfc = _comprobante.emisor_rfc
            comprobante.emisor_nombre = _comprobante.emisor_nombre
            comprobante.emisor_calle = _comprobante.emisor_calle
            comprobante.emisor_noExterior = _comprobante.emisor_noExterior
            comprobante.emisor_noInterior = _comprobante.emisor_noInterior
            comprobante.emisor_colonia = _comprobante.emisor_colonia
            comprobante.emisor_localidad = _comprobante.emisor_localidad
            comprobante.emisor_municipio = _comprobante.emisor_municipio
            comprobante.emisor_estado = _comprobante.emisor_estado
            comprobante.emisor_pais = _comprobante.emisor_pais
            comprobante.emisor_codigoPostal = _comprobante.emisor_codigoPostal
            comprobante.emisor_expedidoEn_calle = _comprobante.emisor_expedidoEn_calle
            comprobante.emisor_expedidoEn_noExterior = _comprobante.emisor_expedidoEn_noExterior
            comprobante.emisor_expedidoEn_noInterior = _comprobante.emisor_expedidoEn_noInterior
            comprobante.emisor_expedidoEn_colonia = _comprobante.emisor_expedidoEn_colonia
            comprobante.emisor_expedidoEn_municipio = _comprobante.emisor_expedidoEn_municipio
            comprobante.emisor_expedidoEn_estado = _comprobante.emisor_expedidoEn_estado
            comprobante.emisor_expedidoEn_pais = _comprobante.emisor_expedidoEn_pais
            comprobante.emisor_regimen = _comprobante.emisor_regimen
            comprobante.receptor_rfc = _comprobante.receptor_rfc
            comprobante.receptor_nombre = _comprobante.receptor_nombre
            comprobante.receptor_calle = _comprobante.receptor_calle
            comprobante.receptor_noExterior = _comprobante.receptor_noExterior
            comprobante.receptor_noInterior = _comprobante.receptor_noInterior
            comprobante.receptor_colonia = _comprobante.receptor_colonia
            comprobante.receptor_localidad = _comprobante.receptor_localidad
            comprobante.receptor_municipio = _comprobante.receptor_municipio
            comprobante.receptor_estado = _comprobante.receptor_estado
            comprobante.receptor_pais = _comprobante.receptor_pais
            comprobante.receptor_codigoPostal = _comprobante.receptor_codigoPostal
            comprobante.conceptos = json.dumps(_comprobante.conceptos)
            comprobante.totalImpuestosTrasladados = _comprobante.totalImpuestosTrasladados
            comprobante.totalImpuestosRetenidos = _comprobante.totalImpuestosRetenidos
            comprobante.impuestos_trasladados = json.dumps(
                _comprobante.impuestos_trasladados
            )
            comprobante.impuestos_retenidos = json.dumps(
                _comprobante.impuestos_retenidos
            )
            comprobante.uuid = _comprobante.uuid
            comprobante.fechaTimbrado = _comprobante.fechaTimbrado
            comprobante.noCertificadoSAT = _comprobante.noCertificadoSAT
            comprobante.selloSAT = _comprobante.selloSAT
            comprobante.save()

            print "Se actualizo el comprobante: {}".format(_comprobante.uuid)

        except Exception as error:

            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )


class ModeloComprobanteEmpleado(object):

    @classmethod
    def add(self, _comprobante):
        import ipdb; ipdb.set_trace()
        origin = "ModeloComprobanteEmpleado.add()"
        try:
            connection.close()
            comprobante = ComprobanteEmpleado(
                serie=_comprobante.serie,
                folio=_comprobante.folio,
                fecha=_comprobante.fecha,
                formaDePago=_comprobante.formaDePago,
                noCertificado=_comprobante.noCertificado,
                subTotal=_comprobante.subTotal,
                tipoCambio=_comprobante.tipoCambio,
                moneda=_comprobante.moneda,
                sello=_comprobante.sello,
                total=_comprobante.total,
                tipoDeComprobante=_comprobante.tipoDeComprobante,
                metodoDePago=_comprobante.metodoDePago,
                lugarExpedicion=_comprobante.lugarExpedicion,
                numCtaPago=_comprobante.numCtaPago,
                condicionesDePago=_comprobante.condicionesDePago,
                emisor_rfc=_comprobante.emisor_rfc,
                emisor_nombre=_comprobante.emisor_nombre,
                emisor_calle=_comprobante.emisor_calle,
                emisor_noExterior=_comprobante.emisor_noExterior,
                emisor_noInterior=_comprobante.emisor_noInterior,
                emisor_colonia=_comprobante.emisor_colonia,
                emisor_localidad=_comprobante.emisor_localidad,
                emisor_municipio=_comprobante.emisor_municipio,
                emisor_estado=_comprobante.emisor_estado,
                emisor_pais=_comprobante.emisor_pais,
                emisor_codigoPostal=_comprobante.emisor_codigoPostal,
                emisor_expedidoEn_calle=_comprobante.emisor_expedidoEn_calle,
                emisor_expedidoEn_noExterior=_comprobante.emisor_expedidoEn_noExterior,
                emisor_expedidoEn_noInterior=_comprobante.emisor_expedidoEn_noInterior,
                emisor_expedidoEn_colonia=_comprobante.emisor_expedidoEn_colonia,
                emisor_expedidoEn_municipio=_comprobante.emisor_expedidoEn_municipio,
                emisor_expedidoEn_estado=_comprobante.emisor_expedidoEn_estado,
                emisor_expedidoEn_pais=_comprobante.emisor_expedidoEn_pais,
                emisor_regimen=_comprobante.emisor_regimen,
                receptor_rfc=_comprobante.receptor_rfc,
                receptor_nombre=_comprobante.receptor_nombre,
                receptor_calle=_comprobante.receptor_calle,
                receptor_noExterior=_comprobante.receptor_noExterior,
                receptor_noInterior=_comprobante.receptor_noInterior,
                receptor_colonia=_comprobante.receptor_colonia,
                receptor_localidad=_comprobante.receptor_localidad,
                receptor_municipio=_comprobante.receptor_municipio,
                receptor_estado=_comprobante.receptor_estado,
                receptor_pais=_comprobante.receptor_pais,
                receptor_codigoPostal=_comprobante.receptor_codigoPostal,
                receptor_jde_clave=_comprobante.numEmpleado,
                conceptos=json.dumps(_comprobante.conceptos),
                totalImpuestosTrasladados=_comprobante.totalImpuestosTrasladados,
                totalImpuestosRetenidos=_comprobante.totalImpuestosRetenidos,
                impuestos_trasladados=json.dumps(
                    _comprobante.impuestos_trasladados),
                impuestos_retenidos=json.dumps(
                    _comprobante.impuestos_retenidos),
                uuid=_comprobante.uuid,
                fechaTimbrado=_comprobante.fechaTimbrado,
                noCertificadoSAT=_comprobante.noCertificadoSAT,
                selloSAT=_comprobante.selloSAT,
                tipoNomina =_comprobante.tipoNomina,
                totalDeducciones =_comprobante.totalDeducciones,
                totalPercepciones =_comprobante.totalPercepciones,
                version =_comprobante.version,
                cveEntidadFederativa =_comprobante.cveEntidadFederativa,
                cuentaBancaria=_comprobante.cuentaBancaria,
                departamento=_comprobante.departamento,
                salarioBaseCotApor =_comprobante.salarioBaseCotApor,
                sindicalizado =_comprobante.sindicalizado ,
                tipoContrato =_comprobante.tipoContrato ,
                registroPatronal = _comprobante.registroPatronal,
                numEmpleado = _comprobante.numEmpleado,
                curp = _comprobante.curp,
                tipoRegimen = _comprobante.tipoRegimen,
                numSeguridadSocial = _comprobante.numSeguridadSocial,
                fechaPago = _comprobante.fechaPago,
                fechaInicialPago = _comprobante.fechaInicialPago,
                fechaFinalPago = _comprobante.fechaFinalPago,
                numDiasPagados = _comprobante.numDiasPagados,
                clabe = _comprobante.clabe,
                banco = _comprobante.banco,
                fechaInicioRelLaboral = _comprobante.fechaInicioRelLaboral,
                antiguedad = _comprobante.antiguedad,
                puesto = _comprobante.puesto,
                tipoJornada = _comprobante.tipoJornada,
                periodicidadPago = _comprobante.periodicidadPago,
                riesgoPuesto = _comprobante.riesgoPuesto,
                salarioDiarioIntegrado = _comprobante.salarioDiarioIntegrado,
                percepciones_totalGravado = _comprobante.percepciones_totalGravado,
                percepciones_totalExento = _comprobante.percepciones_totalExento,
                percepciones = _comprobante.percepciones,
                deducciones_totalGravado = _comprobante.totalDeducciones if _comprobante.version == '1.2' else _comprobante.deducciones_totalGravado,
                deducciones_totalExento = 0.0 if _comprobante.version == '1.2' else _comprobante.deducciones_totalExento,
                deducciones = _comprobante.deducciones,
                horasExtras = _comprobante.horasExtras
            )

            empresa = Empresa.objects.get(clave=_comprobante.empresa_clave)
            comprobante.empresa = empresa
            comprobante.save()

            comprobante.archivo_xml.save(_comprobante.nombre, File(open(_comprobante.get_Abspath(), 'r')))

            print "Se guardo el comprobante: {}".format(_comprobante.uuid)

        except Exception as error:

            if type(error).__name__ == "IntegrityError":

                raise Error(
                    "validacion",
                    origin,
                    "registro ya existe",
                    str(error)
                )

            else:
                raise Error(
                    type(error).__name__,
                    origin,
                    "",
                    str(error)
                )

    @classmethod
    def get(self, _uuid):

        origin = "ModeloComprobanteEmpleado.get()"

        try:
            connection.close()
            factura = ComprobanteEmpleado.objects.get(uuid=_uuid)
            return factura

        except Exception as error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    @classmethod
    def update_SatStatus(self, _comprobante):

        origin = "ModeloComprobanteEmpleado.update_SatStatus()"

        try:
            connection.close()
            comprobante = ComprobanteEmpleado.objects.get(uuid=_comprobante.uuid)
            comprobante.estadoSat = _comprobante.estadoSat
            comprobante.fecha_validacion = _comprobante.fecha_validacion
            comprobante.save()

            print "Se actualizo el comprobante: {}".format(_comprobante.uuid)

        except Exception as error:

            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    @classmethod
    def update_Comprobacion(self, _comprobante):

        origin = "ModeloComprobanteEmpleado.update_Comprobacion()"

        try:
            connection.close()
            comprobante = ComprobanteEmpleado.objects.get(uuid=_comprobante.uuid)
            comprobante.comprobacion = _comprobante.comprobacion

            file_name = _comprobante.nombre.replace(
                'xml',
                'pdf'
            ).replace(
                'XML',
                'PDF'
            )

            file_abspath = _comprobante.get_Abspath().replace(
                'xml',
                'pdf'
            ).replace(
                'XML',
                'PDF'
            )

            comprobante.archivo_pdf.save(file_name, File(open(file_abspath, 'r')))
            # comprobante.save()

            print "Se actualizo el comprobante: {}".format(_comprobante.uuid)

        except Exception as error:

            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    @classmethod
    def update(self, _comprobante):

        origin = "ModeloComprobanteEmpleado.update()"

        try:
            connection.close()

            comprobante = ComprobanteEmpleado.objects.get(uuid=_comprobante.uuid)
            comprobante.serie = _comprobante.serie
            comprobante.folio = _comprobante.folio
            comprobante.fecha = _comprobante.fecha
            comprobante.formaDePago = _comprobante.formaDePago
            comprobante.noCertificado = _comprobante.noCertificado
            comprobante.subTotal = _comprobante.subTotal
            comprobante.tipoCambio = _comprobante.tipoCambio
            comprobante.moneda = _comprobante.moneda
            comprobante.sello = _comprobante.sello
            comprobante.total = _comprobante.total
            comprobante.tipoDeComprobante = _comprobante.tipoDeComprobante
            comprobante.metodoDePago = _comprobante.metodoDePago
            comprobante.lugarExpedicion = _comprobante.lugarExpedicion
            comprobante.numCtaPago = _comprobante.numCtaPago
            comprobante.condicionesDePago = _comprobante.condicionesDePago
            comprobante.emisor_rfc = _comprobante.emisor_rfc
            comprobante.emisor_nombre = _comprobante.emisor_nombre
            comprobante.emisor_calle = _comprobante.emisor_calle
            comprobante.emisor_noExterior = _comprobante.emisor_noExterior
            comprobante.emisor_noInterior = _comprobante.emisor_noInterior
            comprobante.emisor_colonia = _comprobante.emisor_colonia
            comprobante.emisor_localidad = _comprobante.emisor_localidad
            comprobante.emisor_municipio = _comprobante.emisor_municipio
            comprobante.emisor_estado = _comprobante.emisor_estado
            comprobante.emisor_pais = _comprobante.emisor_pais
            comprobante.emisor_codigoPostal = _comprobante.emisor_codigoPostal
            comprobante.emisor_expedidoEn_calle = _comprobante.emisor_expedidoEn_calle
            comprobante.emisor_expedidoEn_noExterior = _comprobante.emisor_expedidoEn_noExterior
            comprobante.emisor_expedidoEn_noInterior = _comprobante.emisor_expedidoEn_noInterior
            comprobante.emisor_expedidoEn_colonia = _comprobante.emisor_expedidoEn_colonia
            comprobante.emisor_expedidoEn_municipio = _comprobante.emisor_expedidoEn_municipio
            comprobante.emisor_expedidoEn_estado = _comprobante.emisor_expedidoEn_estado
            comprobante.emisor_expedidoEn_pais = _comprobante.emisor_expedidoEn_pais
            comprobante.emisor_regimen = _comprobante.emisor_regimen
            comprobante.receptor_rfc = _comprobante.receptor_rfc
            comprobante.receptor_nombre = _comprobante.receptor_nombre
            comprobante.receptor_calle = _comprobante.receptor_calle
            comprobante.receptor_noExterior = _comprobante.receptor_noExterior
            comprobante.receptor_noInterior = _comprobante.receptor_noInterior
            comprobante.receptor_colonia = _comprobante.receptor_colonia
            comprobante.receptor_localidad = _comprobante.receptor_localidad
            comprobante.receptor_municipio = _comprobante.receptor_municipio
            comprobante.receptor_estado = _comprobante.receptor_estado
            comprobante.receptor_pais = _comprobante.receptor_pais
            comprobante.receptor_codigoPostal = _comprobante.receptor_codigoPostal
            comprobante.conceptos = json.dumps(_comprobante.conceptos)
            comprobante.totalImpuestosTrasladados = _comprobante.totalImpuestosTrasladados
            comprobante.totalImpuestosRetenidos = _comprobante.totalImpuestosRetenidos
            comprobante.impuestos_trasladados = json.dumps(
                _comprobante.impuestos_trasladados
            )
            comprobante.impuestos_retenidos = json.dumps(
                _comprobante.impuestos_retenidos
            )
            comprobante.uuid = _comprobante.uuid
            comprobante.fechaTimbrado = _comprobante.fechaTimbrado
            comprobante.noCertificadoSAT = _comprobante.noCertificadoSAT
            comprobante.selloSAT = _comprobante.selloSAT
            registroPatronal = _comprobante.registroPatronal
            numEmpleado = _comprobante.numEmpleado
            curp = _comprobante.curp
            tipoRegimen = _comprobante.tipoRegimen
            numSeguridadSocial = _comprobante.numSeguridadSocial
            fechaPago = _comprobante.fechaPago
            fechaInicialPago = _comprobante.fechaInicialPago
            fechaFinalPago = _comprobante.fechaFinalPago
            numDiasPagados = _comprobante.numDiasPagados
            clabe = _comprobante.clabe
            banco = _comprobante.banco
            fechaInicioRelLaboral = _comprobante.fechaInicioRelLaboral
            antiguedad = _comprobante.antiguedad
            puesto = _comprobante.puesto
            tipoJornada = _comprobante.tipoJornada
            periodicidadPago = _comprobante.periodicidadPago
            riesgoPuesto = _comprobante.riesgoPuesto
            salarioDiarioIntegrado = _comprobante.salarioDiarioIntegrado
            percepciones_totalGravado = _comprobante.percepciones_totalGravado
            percepciones_totalExento = _comprobante.percepciones_totalExento
            percepciones = _comprobante.percepciones
            deducciones_totalGravado = _comprobante.deducciones_totalGravado
            deducciones_totalExento = _comprobante.deducciones_totalExento
            deducciones = _comprobante.deducciones
            horasExtras = _comprobante.horasExtras

            comprobante.save()

            print "Se actualizo el comprobante: {}".format(_comprobante.uuid)

        except Exception as error:

            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )


class ModeloF5903000(object):

    @classmethod
    def add(self, _comprobante):

        origin = "ModeloF5903000.add()"

        try:
            connection.close()
            registro = F5903000(

                ftgenkey=_comprobante.uuid,
                fttax=_comprobante.emisor_rfc,
                fttaxs=_comprobante.receptor_rfc,
                ftbrtpo="CXP",
                ftcrcd=_comprobante.moneda[0:3],
                ftcrr=Validator.convert_ToFloat(_comprobante.tipoCambio),
                ftamrt1=Validator.convert_ToFloat(_comprobante.total) * 10000,
                ftamrt2=Validator.convert_ToFloat(_comprobante.subTotal) * 10000,
                ftamrt3=Validator.convert_ToFloat(_comprobante.total) * 10000,
                fturcd=0,
                ftupmj=Validator.convert_ToJulianJDE(datetime.now().date()),
                ftlo01='5',
                ftuser='ENDTOEND',
                ftpid='SYNFAC',
                ftjobn='ENDTOEND',
                ftivd=Validator.convert_ToJulianJDE(_comprobante.fecha),
                ftan8=_comprobante.emisor_jde_clave
            )

            # ftan8 = _comprobante.getClaveProveedorJDE()

            registro.save(using="jde_p")
            return "Se guardo el comprobante: {}".format(_comprobante.uuid)

        except Exception as error:

            if type(error).__name__ == "IntegrityError":

                raise Error(
                    "validacion",
                    origin,
                    "registro ya existe",
                    str(error)
                )

            else:
                raise Error(
                    type(error).__name__,
                    origin,
                    "",
                    str(error)
                )


class ModeloF0101(object):

    @classmethod
    def get_ByRfc(self, _rfc):

        origin = "ModeloF0101.get()"

        try:
            connection.close()
            registro = F0101.objects.using('jde_p').get(rfc__contains=_rfc, tipo__contains="V")
            return registro

        except Exception as error:

            if type(error).__name__ == 'DoesNotExist':
                raise Error(
                    "validacion",
                    origin,
                    "no proveedor",
                    "No se encontro proveedor %s" % (_rfc)
                )

            else:
                raise Error(
                    type(error).__name__,
                    origin,
                    "",
                    str(error)
                )


class ModeloEmailAccount(object):

    @classmethod
    def get_ByClave(self, _clave):

        origin = "ModeloEmailAccount.get_ByClave()"

        try:
            connection.close()
            registro = EmailAccount.objects.get(clave=_clave)
            return registro

        except Exception as error:

            if type(error).__name__ == 'DoesNotExist':
                raise Error(
                    "validacion",
                    origin,
                    "no proveedor",
                    "No se encontro cuenta %s" % (_clave)
                )

            else:
                raise Error(
                    type(error).__name__,
                    origin,
                    "",
                    str(error)
                )
