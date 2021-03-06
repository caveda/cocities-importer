import os


class Query():
    """ Entity representing a request """

    def __init__(self, uri_path, body=None, headers=None):
        self.uri = os.environ["SERVICE_HOST"] + uri_path
        if headers is not None:
            self.headers = headers
        if body is not None:
            self.body = body
            self.method = "POST"

    headers = None
    body = None
    method = "GET"


"""
    Common constants for cocities requests
"""
URI_SERVICE_COCITIES = """wfsCocities"""
URI_SERVICE_GS = """GsService/Main?gsservice=ls&gsrequest=geojson"""
URI_SERVICE_SOAP = """WebServicesBilbao/services/ws_bilbaoSOAP"""
URI_SERVICE_WS = """WebServicesBilbao/WSBilbao"""
TOKEN_LINE_ID = "[LINEID]"
TOKEN_LINE_CODE = "[LINECODE]"
TOKEN_STOP_ID = "[STOPID]"
TOKEN_DIRECTION_ID = "[DIRID]"
HEADER_SOAPACTION = "SoapAction"
REQUEST_HEADER_COMMON = """<wfs:GetFeature xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.opengis.net/wfshttp://schemas.opengis.net/wfs/1.1.0/wfs.xsd"
      xmlns:gml="http://www.opengis.net/gml" xmlns:wfs="http://www.opengis.net/wfs"
      xmlns:ept="http://namespace.emotion-project.eu/version/Final2.1.0/pubtrans"
      xmlns:ogc="http://www.opengis.net/ogc" service="WFS" version="1.1.0">"""

""" All lines """
REQUEST_BODY_ALL_LINES = """<wfs:Query typeName="ept:Line">
    </wfs:Query>
    </wfs:GetFeature>"""


def get_request_all_lines():
    return Query(URI_SERVICE_COCITIES, REQUEST_HEADER_COMMON + REQUEST_BODY_ALL_LINES)


""" Stops of a line """
REQUEST_BODY_LINE_STOPS_LIST = """<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/"> 
<Body> <wsBilbao xmlns="https://www.bilbao.eus/ws_bilbao/">
<servicio>BUSLISTPAR</servicio>
<usuario>USER</usuario>
<parametros><![CDATA[<?xml version="1.0" encoding="UTF-8"?>
<PETICION><CODIGOLINEA>""" + TOKEN_LINE_ID + """</CODIGOLINEA></PETICION>]]></parametros>
</wsBilbao></Body></Envelope>"""


def get_request_line_stops(id):
    return Query(URI_SERVICE_SOAP,
                 REQUEST_BODY_LINE_STOPS_LIST.replace(TOKEN_LINE_ID, id),
                 {HEADER_SOAPACTION: os.environ["SERVICE_HOST"] + URI_SERVICE_SOAP})


""" Extended information on line stops """
REQUEST_PARAMS_LINE_STOPS_INFO = f'&idservice=parada{TOKEN_LINE_CODE}&json'


def get_request_line_stops_info(code):
    return Query(URI_SERVICE_GS + REQUEST_PARAMS_LINE_STOPS_INFO.replace(TOKEN_LINE_CODE, code))


REQUEST_PARAMS_LINE_ROUTE_MAP = f'&idservice=ruta{TOKEN_LINE_CODE}&json'


def get_request_line_route_map(code):
    """ GPS route of a line """
    return Query(URI_SERVICE_GS + REQUEST_PARAMS_LINE_ROUTE_MAP.replace(TOKEN_LINE_CODE, code))



REQUEST_STOP_STATIC_SCHEDULE = f'?s=BBLISTHORP&u=BILBOBUS&r=JSON&p0={TOKEN_LINE_CODE}&p1={TOKEN_STOP_ID}&p2={TOKEN_DIRECTION_ID}'


def get_request_stop_schedule(line_id, stop_id, direction_code):
    """ Static schedule """
    return Query(URI_SERVICE_WS + REQUEST_STOP_STATIC_SCHEDULE.
                 replace(TOKEN_LINE_CODE, line_id).
                 replace(TOKEN_STOP_ID, stop_id).
                 replace(TOKEN_DIRECTION_ID, direction_code))
