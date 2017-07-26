

# Other's Libraries
from requests import Request
from requests import Session
from xml.etree import ElementTree

# Own's Libraries
from LibTools.data import Error


class WebServiceSAT(object):

    def __init__(self):

        self.webservice = 'https://consultaqr.facturaelectronica.sat.gob.mx/consultacfdiservice.svc'
        self.mensajeSoap = """<?xml version="1.0" encoding="UTF-8"?>
                            <soap:Envelope
                                xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
                                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                                <soap:Header/>
                                <soap:Body>
                                <Consulta xmlns="http://tempuri.org/">
                                    <expresionImpresa>
                                        ?re={0}&amp;rr={1}&amp;tt={2}&amp;id={3}
                                    </expresionImpresa>
                                </Consulta>
                                </soap:Body>
                            </soap:Envelope>"""

    def get_Estado(self, emisor_rfc, receptor_rfc, total, uuid):
        """ Posibles valores de retorno:
            Vigente
            Cancelado
            Desconocido
        """
        origin = "WebServiceSAT.get_Estado()"

        datos = self.mensajeSoap.format(emisor_rfc, receptor_rfc, total, uuid).encode('utf-8')
        cabecera = {
            'SOAPAction': '"http://tempuri.org/IConsultaCFDIService/Consulta"',
            'Content-length': len(datos),
            'Content-type': 'text/xml; charset="UTF-8"'
        }
        sesion_ = Session()
        request_ = Request('POST', self.webservice, data=datos, headers=cabecera)
        prepped = request_.prepare()

        try:

            response = sesion_.send(prepped, timeout=5)
            tree = ElementTree.fromstring(response.text)
            estado = tree[0][0][0][1].text
            return estado

        except Exception, error:

            raise Error(
                type(error).__name__,
                origin,
                "",
                str(error)
            )
