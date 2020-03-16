import requests
import broker.cocities
from broker import cocities
import re
from xml.dom import minidom

from broker.model import Line, LINE_FORWARD_DIRECTION
from broker.parser_lines import parse_lines

"""
    Returns the complete list of lines without stops or routes.
"""
def get_all_lines():
    query = cocities.get_request_all_lines()
    req = send_http_request(query)
    req.encoding = 'utf-8' # force utf-8 encoding to preserve special chars
    lines = parse_lines(req.text)
    for l in lines:
        print(l.json())



"""
    Build a request out of the passed query. 
"""
def send_http_request (query):
    return requests.request(query.method,
                            url = query.uri,
                            headers = query.headers,
                            data = query.body)


