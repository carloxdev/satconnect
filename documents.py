# -*- coding: utf-8 -*-

# Python's Libraries
import os

# Other's Libraries
from lxml import etree

# Own's Libraries
from LibTools.filesystem import Archivo
from LibTools.data import Error
from LibTools.data import Validator


class Comprobante(Archivo):

    def __init__(self, _folder, _name):

        Archivo.__init__(self, _folder, _name)

        # Comprobante
        self.serie = ''
        self.folio = ''
        self.fecha = ''
        self.formaDePago = ''
        self.noCertificado = ''
        self.subTotal = '0'
        self.tipoCambio = '1'
        self.moneda = ''
        self.sello = ''
        self.total = '0'
        self.tipoDeComprobante = ''
        self.metodoDePago = ''
        self.lugarExpedicion = ''
        self.numCtaPago = ''
        self.condicionesDePago = ''

        # Emisor
        self.emisor_rfc = ''
        self.emisor_nombre = ''

        # Emisor Direccion
        self.emisor_calle = ''
        self.emisor_noExterior = ''
        self.emisor_noInterior = ''
        self.emisor_colonia = ''
        self.emisor_localidad = ''
        self.emisor_municipio = ''
        self.emisor_estado = ''
        self.emisor_pais = ''
        self.emisor_codigoPostal = ''

        # Emisor Expedido en
        self.emisor_expedidoEn_calle = ''
        self.emisor_expedidoEn_noExterior = ''
        self.emisor_expedidoEn_noInterior = ''
        self.emisor_expedidoEn_colonia = ''
        self.emisor_expedidoEn_municipio = ''
        self.emisor_expedidoEn_estado = ''
        self.emisor_expedidoEn_pais = ''

        # Emisor Regimen
        self.emisor_regimen = ''

        # Receptor
        self.receptor_rfc = ''
        self.receptor_nombre = ''

        # Receptor Direccion
        self.receptor_calle = ''
        self.receptor_noExterior = ''
        self.receptor_noInterior = ''
        self.receptor_colonia = ''
        self.receptor_localidad = ''
        self.receptor_municipio = ''
        self.receptor_estado = ''
        self.receptor_pais = ''
        self.receptor_codigoPostal = ''

        # Conceptos
        self.conceptos = []

        # Impuestos
        self.totalImpuestosTrasladados = '0'
        self.totalImpuestosRetenidos = '0'

        # Impuestos Trasladados
        self.impuestos_trasladados = []

        # Impuestos Retenidos
        self.impuestos_retenidos = []

        # Complementos
        self.uuid = ''
        self.fechaTimbrado = ''
        self.noCertificadoSAT = ''
        self.selloSAT = ''

        # Nomina Datos
        #1.2
        self.tipoNomina = ''
        self.totalDeducciones = ''
        self.totalPercepciones = ''
        self.version = ''
        self.cveEntidadFederativa = ''
        self.cuentaBancaria= ''
        self.departamento= ''
        self.salarioBaseCotApor = ''
        self.sindicalizado = ''
        self.tipoContrato = ''
        #/1.2
        self.registroPatronal = ''
        self.numEmpleado = ''
        self.curp = ''
        self.tipoRegimen = ''
        self.numSeguridadSocial = ''
        self.fechaPago = ''
        self.fechaInicialPago = ''
        self.fechaFinalPago = ''
        self.numDiasPagados = ''
        self.clabe = ''
        self.banco = ''
        self.fechaInicioRelLaboral = ''
        self.antiguedad = ''
        self.puesto = ''
        self.tipoJornada = ''
        self.periodicidadPago = ''
        self.riesgoPuesto = ''
        self.salarioDiarioIntegrado = '0'

        # Nomina Percepciones
        self.percepciones_totalGravado = '0'
        self.percepciones_totalExento = '0'
        #1.2
        self.percepciones_totalSueldos = '0'
        #/1.2
        self.percepciones = []

        # Nomina Deducciones
        self.deducciones_totalGravado = '0'
        self.deducciones_totalExento = '0'
        #1.2
        self.deducciones_totalImpuestosRetenidos = '0'
        self.deducciones_totalOtrasDeducciones = '0'
        #/1.2
        self.deducciones = []

        # Horas Extras
        self.horasExtras = []

        # Otros campos
        self.empresa_clave = ''
        self.resumen_tipo = 'UNKNOWN'
        self.comprobacion = "NRE"
        self.estadoSat = "SIN VALIDAR"
        self.fecha_validacion = ''

        self.raiz = None
        self.name_spaces = None

        self.init()

    def init(self):

        origin = "Comprobante.init()"

        try:

            recovering_parser = etree.XMLParser(recover=True)

            if os.path.isfile(self.get_Abspath()):

                document = etree.parse(self.get_Abspath(), parser=recovering_parser)
                self.raiz = document.getroot()

                self.name_spaces = {
                    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                    'cfdi': 'http://www.sat.gob.mx/cfd/3',
                    'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital',
                    'nomina': 'http://www.sat.gob.mx/nomina',
                    'nomina12': 'http://www.sat.gob.mx/nomina12'
                }

        except Exception, error:

            if type(error).__name__ == "XMLSyntaxError":
                raise Error(
                    "validacion",
                    origin,
                    "xml corrupto",
                    str(error)
                )

            else:
                raise Error(
                    type(error).__name__,
                    origin,
                    "",
                    str(error)
                )

    def get_Value_Nodo(self, _node, _list, _type, _default=0):

        value = None

        for item in _list:
            if _node.get(item):
                value = _node.get(item)

        if _type == "char":
            value = Validator.convert_ToChar(value)
        elif _type == "float":
            value = Validator.convert_ToFloat(value, _default)
        elif _type == "int":
            value = Validator.convert_ToInt(value)
        elif _type == "date":
            value = Validator.convert_ToDate(value)
        else:
            value = value

        return value

    def read_Comprobante_Node(self):

        origin = "Comprobante.read_Comprobante_Node()"

        try:
            self.serie = self.get_Value_Nodo(self.raiz, ['serie', 'Serie'], "char")
            self.folio = self.get_Value_Nodo(self.raiz, ['folio', 'Folio'], "char")
            self.fecha = self.get_Value_Nodo(self.raiz, ['fecha', 'Fecha'], "date")
            self.formaDePago = self.get_Value_Nodo(self.raiz, ['formaDePago', 'FormaPago'], "char")
            self.noCertificado = self.get_Value_Nodo(self.raiz, ['noCertificado', 'NoCertificado'], "char")
            self.subTotal = self.get_Value_Nodo(self.raiz, ['subTotal', 'SubTotal'], "float")
            self.tipoCambio = self.get_Value_Nodo(self.raiz, ['TipoCambio'], "float", 1)
            self.moneda = self.get_Value_Nodo(self.raiz, ['Moneda'], "char")
            self.sello = self.get_Value_Nodo(self.raiz, ['sello', 'Sello'], "char")
            self.total = self.get_Value_Nodo(self.raiz, ['total', 'Total'], "float")
            self.tipoDeComprobante = self.get_Value_Nodo(self.raiz, ['tipoDeComprobante', 'TipoDeComprobante'], "char")
            self.metodoDePago = self.get_Value_Nodo(self.raiz, ['metodoDePago', 'MetodoPago'], "char")
            self.lugarExpedicion = self.get_Value_Nodo(self.raiz, ['LugarExpedicion'], "char")
            self.numCtaPago = self.get_Value_Nodo(self.raiz, ['NumCtaPago'], "char")
            self.condicionesDePago = self.get_Value_Nodo(self.raiz, ['condicionesDePago', 'CondicionesDePago'], "char")

            return True

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    def read_Emisor_Node(self):

        origin = "Comprobante.read_Emisor_Node()"

        try:
            # Obtener nodo
            nodo = self.raiz.find(
                'cfdi:Emisor',
                self.name_spaces
            )

            self.emisor_rfc = self.get_Value_Nodo(nodo, ['rfc', 'Rfc'], "char").upper()
            self.emisor_nombre = self.get_Value_Nodo(nodo, ['nombre', 'Nombre'], "char").upper()
            self.emisor_regimen = self.get_Value_Nodo(nodo, ['RegimenFiscal'], "char")

            return True

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    def read_Emisor_DomicilioFiscal_Node(self):

        origin = "Comprobante.read_Emisor_DomicilioFiscal_Node()"

        try:

            # obtener nodo
            nodo = self.raiz.find('cfdi:Emisor', self.name_spaces).find(
                'cfdi:DomicilioFiscal',
                self.name_spaces
            )

            # obtener datos
            self.emisor_calle = self.get_Value_Nodo(nodo, ['calle'], "char")
            self.emisor_noExterior = self.get_Value_Nodo(nodo, ['noExterior'], "char")
            self.emisor_noInterior = self.get_Value_Nodo(nodo, ['noInterior'], "char")
            self.emisor_colonia = self.get_Value_Nodo(nodo, ['colonia'], "char")
            self.emisor_localidad = self.get_Value_Nodo(nodo, ['localidad'], "char")
            self.emisor_municipio = self.get_Value_Nodo(nodo, ['municipio'], "char")
            self.emisor_estado = self.get_Value_Nodo(nodo, ['estado'], "char")
            self.emisor_pais = self.get_Value_Nodo(nodo, ['pais'], "char")
            self.emisor_codigoPostal = self.get_Value_Nodo(nodo, ['codigoPostal'], "int")

            return True

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    def read_Emisor_ExpedidoEn_Node(self):

        origin = "Comprobante.read_Emisor_ExpedidoEn_Node()"

        try:

            # obtener nodo
            nodo = self.raiz.find('cfdi:Emisor', self.name_spaces).find(
                'cfdi:ExpedidoEn',
                self.name_spaces
            )

            # obtener datos
            self.emisor_expedidoEn_calle = self.get_Value_Nodo(nodo, ['calle'], "char")
            self.emisor_expedidoEn_noExterior = self.get_Value_Nodo(nodo, ['noExterior'], "char")
            self.emisor_expedidoEn_noInterior = self.get_Value_Nodo(nodo, ['noInterior'], "char")
            self.emisor_expedidoEn_colonia = self.get_Value_Nodo(nodo, ['colonia'], "char")
            self.emisor_expedidoEn_municipio = self.get_Value_Nodo(nodo, ['municipio'], "char")
            self.emisor_expedidoEn_estado = self.get_Value_Nodo(nodo, ['estado'], "char")
            self.emisor_expedidoEn_pais = self.get_Value_Nodo(nodo, ['pais'], "char")

            return True

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    def read_Emisor_RegimenFiscal_Node(self):

        origin = "Comprobante.read_Emisor_RegimenFiscal_Node()"

        try:
            nodo = self.raiz.find('cfdi:Emisor', self.name_spaces).find(
                'cfdi:RegimenFiscal',
                self.name_spaces
            )
            self.emisor_regimen = self.get_Value_Nodo(nodo, ['Regimen'], "char")

            return True

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    def read_Receptor_Node(self):

        origin = "Comprobante.read_Receptor_Node()"

        try:

            nodo = self.raiz.find(
                'cfdi:Receptor',
                self.name_spaces
            )

            self.receptor_rfc = self.get_Value_Nodo(nodo, ['rfc', 'Rfc'], "char")
            self.receptor_nombre = self.get_Value_Nodo(nodo, ['nombre', 'Nombre'], "char")

            return True

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    def read_Receptor_Domicilio_Node(self):

        origin = "Comprobante.read_Receptor_Domicilio_Node()"

        try:

            nodo = self.raiz.find('cfdi:Receptor', self.name_spaces).find(
                'cfdi:Domicilio',
                self.name_spaces
            )

            self.receptor_calle = self.get_Value_Nodo(nodo, ['calle'], "char")
            self.receptor_noExterior = self.get_Value_Nodo(nodo, ['noExterior'], "char")
            self.receptor_noInterior = self.get_Value_Nodo(nodo, ['noInterior'], "char")
            self.receptor_colonia = self.get_Value_Nodo(nodo, ['colonia'], "char")
            self.receptor_localidad = self.get_Value_Nodo(nodo, ['localidad'], "char")
            self.receptor_municipio = self.get_Value_Nodo(nodo, ['municipio'], "char")
            self.receptor_estado = self.get_Value_Nodo(nodo, ['estado'], "char")
            self.receptor_pais = self.get_Value_Nodo(nodo, ['pais'], "char")
            self.receptor_codigoPostal = self.get_Value_Nodo(nodo, ['codigoPostal'], "char")

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    def read_Impuestos_Node(self):

        origin = "Comprobante.read_Impuestos_Node()"

        try:

            nodo = self.raiz.find('cfdi:Impuestos', self.name_spaces)

            self.totalImpuestosTrasladados = self.get_Value_Nodo(nodo, ['totalImpuestosTrasladados'], "float")
            self.totalImpuestosRetenidos = self.get_Value_Nodo(nodo, ['totalImpuestosRetenidos'], "float")

            return True

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    def read_Impuestos_Traslados(self):

        origin = "Comprobante.read_Impuestos_Traslados()"

        try:
            nodo = self.raiz.find('cfdi:Impuestos', self.name_spaces)
            nodos = nodo.find('cfdi:Traslados', self.name_spaces)

            for nodo in nodos:

                impuesto = {
                    'impuesto': self.get_Value_Nodo(nodo, ['impuesto'], "char"),
                    'tasa': self.get_Value_Nodo(nodo, ['tasa'], "char"),
                    'importe': self.get_Value_Nodo(nodo, ['importe'], "char")
                }

                self.impuestos_trasladados.append(impuesto)

            return True

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    def read_Impuestos_Retenciones(self):

        origin = "Comprobante.read_Impuestos_Retenciones()"

        try:
            nodo = self.raiz.find('cfdi:Impuestos', self.name_spaces)
            nodos = nodo.find('cfdi:Retenciones', self.name_spaces)

            for nodo in nodos:

                impuesto = {
                    'impuesto': self.get_Value_Nodo(nodo, ['impuesto'], "char"),
                    'importe': self.get_Value_Nodo(nodo, ['importe'], "char"),
                }

                self.impuestos_retenidos.append(impuesto)

            return True

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    def read_Conceptos_Node(self):

        origin = "Comprobante.read_Impuestos_Retenciones()"

        try:
            nodos = self.raiz.find('cfdi:Conceptos', self.name_spaces)
            for nodo in nodos:
                item = {
                    "cantidad": self.get_Value_Nodo(nodo, ['cantidad'], "char"),
                    "unidad": self.get_Value_Nodo(nodo, ['unidad'], "char"),
                    "noIdentificacion": self.get_Value_Nodo(nodo, ['noIdentificacion'], "char"),
                    "descripcion": self.get_Value_Nodo(nodo, ['descripcion'], "char"),
                    "valorUnitario": self.get_Value_Nodo(nodo, ['valorUnitario'], "char"),
                    "importe": self.get_Value_Nodo(nodo, ['importe'], "char")
                }

                self.conceptos.append(item)

            return True

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    def read_Complemento_Node(self):

        origin = "Comprobante.read_Complemento_Node()"

        try:
            nodo = self.raiz.find('cfdi:Complemento', self.name_spaces).find(
                'tfd:TimbreFiscalDigital',
                self.name_spaces
            )

            self.uuid = self.get_Value_Nodo(nodo, ['UUID'], "char").upper()
            self.fechaTimbrado = self.get_Value_Nodo(nodo, ['FechaTimbrado'], "date")
            self.noCertificadoSAT = self.get_Value_Nodo(nodo, ['noCertificadoSAT', 'NoCertificadoSAT'], "char")
            self.selloSAT = self.get_Value_Nodo(nodo, ['selloSAT', 'SelloSAT'], "char")

            return True

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    def read_Nomina_Node(self):

        origin = "Comprobante.read_Nomina_Node()"

        try:

            nodo = self.raiz.find('cfdi:Complemento', self.name_spaces).find(
                'nomina:Nomina',
                self.name_spaces
            )

            self.registroPatronal = self.get_Value_Nodo(nodo, ['RegistroPatronal'], "char")
            self.numEmpleado = self.get_Value_Nodo(nodo, ['NumEmpleado'], "char")
            self.curp = self.get_Value_Nodo(nodo, ['CURP'], "char")
            self.tipoRegimen = self.get_Value_Nodo(nodo, ['TipoRegimen'], "char")
            self.numSeguridadSocial = self.get_Value_Nodo(nodo, ['NumSeguridadSocial'], "char")
            self.fechaPago = self.get_Value_Nodo(nodo, ['FechaPago'], "date")
            self.fechaInicialPago = self.get_Value_Nodo(nodo, ['FechaInicialPago'], "date")
            self.fechaFinalPago = self.get_Value_Nodo(nodo, ['FechaFinalPago'], "date")
            self.numDiasPagados = self.get_Value_Nodo(nodo, ['NumDiasPagados'], "int")
            self.clabe = self.get_Value_Nodo(nodo, ['CLABE'], "char")
            self.banco = self.get_Value_Nodo(nodo, ['Banco'], "char")
            self.fechaInicioRelLaboral = self.get_Value_Nodo(nodo, ['FechaInicioRelLaboral'], "date")
            self.antiguedad = self.get_Value_Nodo(nodo, ['Antiguedad'], "int")
            self.puesto = self.get_Value_Nodo(nodo, ['Puesto'], "char")
            self.tipoJornada = self.get_Value_Nodo(nodo, ['TipoJornada'], "char")
            self.periodicidadPago = self.get_Value_Nodo(nodo, ['PeriodicidadPago'], "char")
            self.riesgoPuesto = self.get_Value_Nodo(nodo, ['RiesgoPuesto'], "char")
            self.salarioDiarioIntegrado = self.get_Value_Nodo(nodo, ['SalarioDiarioIntegrado'], "float")

            return True

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    def read_Nomina_Percepciones_Node(self):

        origin = "Comprobante.read_Nomina_Percepciones_Node()"

        try:
            nodos = self.raiz.find('cfdi:Complemento', self.name_spaces).find(
                'nomina:Nomina',
                self.name_spaces
            ).find('nomina:Percepciones', self.name_spaces)

            self.percepciones_totalGravado = self.get_Value_Nodo(nodos, ['TotalGravado'], "float")
            self.percepciones_totalExento = self.get_Value_Nodo(nodos, ['TotalExento'], "float")

            for nodo in nodos:
                item = {
                    'TipoPercepcion': self.get_Value_Nodo(nodo, ['TipoPercepcion'], "char"),
                    'Clave': self.get_Value_Nodo(nodo, ['Clave'], "char"),
                    'Concepto': self.get_Value_Nodo(nodo, ['Concepto'], "char"),
                    'ImporteGravado': self.get_Value_Nodo(nodo, ['ImporteGravado'], "char"),
                    'ImporteExento': self.get_Value_Nodo(nodo, ['ImporteExento'], "char")
                }

                self.percepciones.append(item)

            return True

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    def read_Nomina_Deducciones_Node(self):

        origin = "Comprobante.read_Nomina_Deducciones_Node()"

        try:
            nodos = self.raiz.find('cfdi:Complemento', self.name_spaces).find(
                'nomina:Nomina',
                self.name_spaces
            ).find('nomina:Deducciones', self.name_spaces)

            self.deducciones_totalGravado = self.get_Value_Nodo(nodos, ['TotalGravado'], "float")
            self.deducciones_totalExento = self.get_Value_Nodo(nodos, ['TotalExento'], "float")

            for nodo in nodos:
                item = {
                    'TipoDeduccion': self.get_Value_Nodo(nodo, ['TipoDeduccion'], "char"),
                    'Clave': self.get_Value_Nodo(nodo, ['Clave'], "char"),
                    'Concepto': self.get_Value_Nodo(nodo, ['Concepto'], "char"),
                    'ImporteGravado': self.get_Value_Nodo(nodo, ['ImporteGravado'], "char"),
                    'ImporteExento': self.get_Value_Nodo(nodo, ['ImporteExento'], "char")
                }

                self.deducciones.append(item)

            return True

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    def read_Nomina_HorasExtras(self):

        origin = "Comprobante.read_Nomina_HorasExtras()"

        try:
            nodos = self.raiz.find('cfdi:Complemento', self.name_spaces).find(
                'nomina:Nomina',
                self.name_spaces
            ).find('nomina:HorasExtras', self.name_spaces)

            for nodo in nodos:
                item = {
                    'Dias': self.get_Value_Nodo(nodo, ['Dias'], "char"),
                    'TipoHoras': self.get_Value_Nodo(nodo, ['TipoHoras'], "char"),
                    'ImportePagado': self.get_Value_Nodo(nodo, ['ImportePagado'], "char")
                }

                self.horasExtras.append(item)

            return True

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    def read_Nomina12_Node(self):

        origin = "Comprobante.read_Nomina12_Node()"

        try:

            nodo = self.raiz.find('cfdi:Complemento', self.name_spaces).find(
                'nomina12:Nomina',
                self.name_spaces
            )

            #1.2
            self.tipoNomina = self.get_Value_Nodo(nodo, ['TipoNomina'], "char")
            self.totalDeducciones = self.get_Value_Nodo(nodo, ['TotalDeducciones'], "char")
            self.totalPercepciones = self.get_Value_Nodo(nodo, ['TotalPercepciones'], "char")
            self.version = self.get_Value_Nodo(nodo, ['Version'], "char")
            #/1.2
            self.fechaInicialPago = self.get_Value_Nodo(nodo, ['FechaInicialPago'], "date")
            self.fechaFinalPago = self.get_Value_Nodo(nodo, ['FechaFinalPago'], "date")
            self.numDiasPagados = self.get_Value_Nodo(nodo, ['NumDiasPagados'], "float")
            self.fechaPago = self.get_Value_Nodo(nodo, ['FechaPago'], "date")

            return True

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    def read_Nomina12_Emisor_Node(self):

        origin = "Comprobante.read_Nomina12_Emisor_Node()"

        try:
            nodo = self.raiz.find('cfdi:Complemento', self.name_spaces).find(
                'nomina12:Nomina',self.name_spaces).find(
                'nomina12:Emisor', self.name_spaces)

            #1.2
            self.registroPatronal = self.get_Value_Nodo(nodo, ['TipoNomina'], "char")
            #/1.2

            return True

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    def read_Nomina12_Receptor_Node(self):
        origin = "Comprobante.read_Nomina12_Recepror_Node()"

        try:
            nodo = self.raiz.find('cfdi:Complemento', self.name_spaces).find(
                'nomina12:Nomina',
                self.name_spaces
                ).find('nomina12:Receptor', self.name_spaces)
            #1.2
            self.tipoContrato = self.get_Value_Nodo(nodo, ['TipoContrato'], "char")
            self.salarioBaseCotApor = self.get_Value_Nodo(nodo, ['SalarioBaseCotApor'], "float")
            self.cveEntidadFederativa = self.get_Value_Nodo(nodo, ['ClaveEntFed'], "char")
            self.cuentaBancaria= self.get_Value_Nodo(nodo, ['CuentaBancaria'], "char")
            self.departamento= self.get_Value_Nodo(nodo, ['Departamento'], "char")
            #/1.2
            self.curp = self.get_Value_Nodo(nodo, ['CURP','Curp'], "char")
            self.numSeguridadSocial = self.get_Value_Nodo(nodo, ['NumSeguridadSocial'], "char")
            self.fechaInicioRelLaboral = self.get_Value_Nodo(nodo, ['FechaInicioRelLaboral'], "date")
            #self.antiguedad = self.get_Value_Nodo(nodo, ['Antigüedad'], "char")
            self.tipoJornada = self.get_Value_Nodo(nodo, ['TipoJornada'], "char")
            self.tipoRegimen = self.get_Value_Nodo(nodo, ['TipoRegimen'], "char")
            self.numEmpleado = self.get_Value_Nodo(nodo, ['NumEmpleado'], "char")
            self.puesto = self.get_Value_Nodo(nodo, ['Puesto'], "char")
            self.riesgoPuesto = self.get_Value_Nodo(nodo, ['RiesgoPuesto'], "char")
            self.periodicidadPago = self.get_Value_Nodo(nodo, ['PeriodicidadPago'], "char")
            self.salarioDiarioIntegrado = self.get_Value_Nodo(nodo, ['SalarioDiarioIntegrado'], "float")

            return True

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    def read_Nomina12_Percepciones_Node(self):

        origin = "Comprobante.read_Nomina12_Percepciones_Node()"

        try:
            nodos = self.raiz.find('cfdi:Complemento', self.name_spaces).find(
                'nomina12:Nomina',
                self.name_spaces
            ).find('nomina12:Percepciones', self.name_spaces)
            self.percepciones_totalGravado = self.get_Value_Nodo(nodos, ['TotalGravado'], "float")
            self.percepciones_totalExento = self.get_Value_Nodo(nodos, ['TotalExento'], "float")
            self.TotalSueldos = self.get_Value_Nodo(nodos,['TotalSueldos'], "char")

            for nodo in nodos:
                item = {
                    'TipoPercepcion': self.get_Value_Nodo(nodo, ['TipoPercepcion'], "char"),
                    'Clave': self.get_Value_Nodo(nodo, ['Clave'], "char"),
                    'Concepto': self.get_Value_Nodo(nodo, ['Concepto'], "char"),
                    'ImporteGravado': self.get_Value_Nodo(nodo, ['ImporteGravado'], "char"),
                    'ImporteExento': self.get_Value_Nodo(nodo, ['ImporteExento'], "char")
                }

                self.percepciones.append(item)

            return True

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )

    def read_Nomina12_Deducciones_Node(self):

        origin = "Comprobante.read_Nomina12_Deducciones_Node()"

        try:
            nodos = self.raiz.find('cfdi:Complemento', self.name_spaces).find(
                'nomina12:Nomina',
                self.name_spaces
            ).find('nomina12:Deducciones', self.name_spaces)

            self.deducciones_totalOtrasDeducciones = self.get_Value_Nodo(nodos, ['TotalOtrasDeducciones'], "float")
            self.deducciones_totalImpuestosRetenidos = self.get_Value_Nodo(nodos, ['TotalImpuestosRetenidos'], "float")

            for nodo in nodos:
                item = {
                    'TipoDeduccion': self.get_Value_Nodo(nodo, ['TipoDeduccion'], "char"),
                    'Clave': self.get_Value_Nodo(nodo, ['Clave'], "char"),
                    'Concepto': self.get_Value_Nodo(nodo, ['Concepto'], "char"),
                    'Importe': self.get_Value_Nodo(nodo, ['Importe'], "char"),
                }

                self.deducciones.append(item)

            return True

        except Exception, error:
            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )


    def read(self):

        # Se obtienen datos del COMPROBANTE
        try:
            self.read_Comprobante_Node()
            print "Obtiendo datos del nodo COMPROBANTE.............OK"

        except Exception, error:
            print "Obtiendo datos del nodo COMPROBANTE.............{}".format(
                error.mensaje
            )

        # Se obtienen datos del EMISOR
        try:
            self.read_Emisor_Node()
            print "Obtiendo datos del nodo EMISOR..................OK"

        except Exception, error:
            print "Obtiendo datos del nodo EMISOR..................{}".format(
                error.mensaje
            )

        # Se obtienen datos del EMISOR DIRECCION
        try:
            self.read_Emisor_DomicilioFiscal_Node()
            print "Obtiendo datos del nodo EMISOR DIRECCION........OK"

        except Exception, error:
            print "Obtiendo datos del nodo EMISOR DIRECCION........{}".format(
                error.mensaje
            )

        # Se obtienen datos del modo EMISOR EXPEDIDO EN
        try:
            self.read_Emisor_ExpedidoEn_Node()
            print "Obtiendo datos del nodo EMISOR EXPEDIDO EN......OK"

        except Exception, error:
            print "Obtiendo datos del nodo EMISOR EXPEDIDO EN......{}".format(
                error.mensaje
            )

        # Se obtienen datos del nodo EMISOR REGIMEN
        try:
            self.read_Emisor_RegimenFiscal_Node()
            print "Obtiendo datos del nodo EMISOR REGIMEN..........OK"

        except Exception, error:
            print "Obtiendo datos del nodo EMISOR REGIMEN..........{}".format(
                error.mensaje
            )

        # Se obtienen datos del nodo RECEPTOR
        try:
            self.read_Receptor_Node()
            print "Obtiendo datos del nodo RECEPTOR................OK"

        except Exception, error:
            print "Obtiendo datos del nodo RECEPTOR................{}".format(
                error.mensaje
            )

        # Se obtienen datos del nodo RECEPTOR DIRECCION
        try:
            self.read_Receptor_Domicilio_Node()
            print "Obtiendo datos del nodo RECEPTOR DIRECCION......OK"

        except Exception, error:
            print "Obtiendo datos del nodo RECEPTOR DIRECCION......{}".format(
                error.mensaje
            )

        # Se obtienen datos del nodo IMPUESTOS
        try:
            self.read_Impuestos_Node()
            print "Obtiendo datos del nodo IMPUESTOS...............OK"

        except Exception, error:
            print "Obtiendo datos del nodo IMPUESTOS...............{}".format(
                error.mensaje
            )

        # Se obtienen datos del nodo IMPUESTOS TRASLADADOS
        try:
            self.read_Impuestos_Traslados()
            print "Obtiendo datos del nodo IMPUESTOS TRASLADADOS...OK"

        except Exception, error:
            print "Obtiendo datos del nodo IMPUESTOS TRASLADADOS...{}".format(
                error.mensaje
            )

        # Se obtienen datos del nodo IMPUESTOS RETENIDOS
        try:
            self.read_Impuestos_Retenciones()
            print "Obtiendo datos del nodo IMPUESTOS RETENIDOS.....OK"

        except Exception, error:

            print "Obtiendo datos del nodo IMPUESTOS RETENIDOS.....{}".format(
                error.mensaje
            )

        # Se obtienen datos del nodo CONCEPTOS
        try:
            self.read_Conceptos_Node()
            print "Obtiendo datos del nodo CONCEPTOS...............OK"

        except Exception, error:
            print "Obtiendo datos del nodo CONCEPTOS...............{}".format(
                error.mensaje
            )

        # Se obtienen datos del nodo COMPLEMENTO
        try:
            self.read_Complemento_Node()
            print "Obtiendo datos del nodo COMPLEMENTO.............OK"

        except Exception, error:
            print "Obtiendo datos del nodo COMPLEMENTO.............{}".format(
                error.mensaje
            )

        # Se obtienen datos del nodo NOMINA
        try:
            self.read_Nomina_Node()
            print "Obtiendo datos del nodo NOMINA..................OK"

        except Exception, error:
            print "Obtiendo datos del nodo NOMINA..................{}".format(
                error.mensaje
            )
        # Se obtienen datos del nodo PERCEPCIONES
        try:
            self.read_Nomina_Percepciones_Node()
            print "Obtiendo datos del nodo PERCEPCIONES............OK"

        except Exception, error:
            print "Obtiendo datos del nodo PERCEPCIONES............{}".format(
                error.mensaje
            )

        # Se obtienen datos del nodo DEDUCCIONES
        try:
            self.read_Nomina_Deducciones_Node()
            print "Obtiendo datos del nodo DEDUCCIONES.............OK"

        except Exception, error:
            print "Obtiendo datos del nodo DEDUCCIONES.............{}".format(
                error.mensaje
            )

        # Se obtienen datos del nodo HORAS EXTRAS
        try:
            self.read_Nomina_HorasExtras()
            print "Obtiendo datos del nodo HORAS EXTRAS............OK"

        except Exception, error:
            print "Obtiendo datos del nodo HORAS EXTRAS............{}".format(
                error.mensaje
            )


        # Se obtienen datos del nodo NOMINA 1.2
        try:
            self.read_Nomina12_Node()
            print "Obtiendo datos del nodo NOMINA 1.2.............OK"

        except Exception, error:
            print "Obtiendo datos del nodo NOMINA 1.2..............{}".format(
                error.mensaje
            )

        # Se obtienen datos del nodo RECEPTOR 1.2
        try:
            self.read_Nomina12_Receptor_Node()
            print "Obtiendo datos del nodo RECEPTOR 1.2.............OK"

        except Exception, error:
            print "Obtiendo datos del nodo RECEPTOR 1.2..............{}".format(
                error.mensaje
            )

        # Se obtienen datos del nodo EMISOR 1.2
        try:
            self.read_Nomina12_Emisor_Node()
            print "Obtiendo datos del nodo EMISOR 1.2.............OK"

        except Exception, error:
            print "Obtiendo datos del nodo EMISOR 1.2..............{}".format(
                error.mensaje
            )

        # Se obtienen datos del nodo PERCEPCIONES 1.2
        try:
            self.read_Nomina12_Percepciones_Node()
            print "Obtiendo datos del nodo PERCEPCIONES 1.2.............OK"

        except Exception, error:
            print "Obtiendo datos del nodo PERCEPCIONES 1.2..............{}".format(
                error.mensaje
            )

        # Se obtienen datos del nodo DEDUCCIONES 1.2
        try:
            self.read_Nomina12_Deducciones_Node()
            print "Obtiendo datos del nodo DEDUCCIONES 1.2.............OK"

        except Exception, error:
            print "Obtiendo datos del nodo DEDUCCIONES 1.2..............{}".format(
                error.mensaje
            )

    def __str__(self):
        return """
        UUID: {}
        Emisor: {} ({})
        Receptor: {} ({})
        Fecha: {}
        Fecha Timbrado: {}
        """.format(
            self.uuid,
            self.emisor_nombre,
            self.emisor_rfc,
            self.receptor_nombre,
            self.receptor_rfc,
            self.fecha,
            self.fechaTimbrado
        )
