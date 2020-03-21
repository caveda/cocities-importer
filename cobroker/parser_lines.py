from xml.dom import minidom
from cobroker.model import LINE_FORWARD_DIRECTION, Line


def parse_lines(xml_response):
    """ Parse the response of all lines query """
    xmldoc = minidom.parseString(xml_response)
    lines_nodes = xmldoc.getElementsByTagName("ept:Line")
    result = []
    for l in lines_nodes:
        line = Line(parse_line_id(l), parse_line_name(l), LINE_FORWARD_DIRECTION)
        result.append(line)
    return result


def parse_line_id(l):
    """ Parse a line node to get the line ID """
    id_node = l.getElementsByTagName("ept:LineCode")[0].getElementsByTagName("ept:identifier")
    return id_node[0].firstChild.data


def parse_line_name(l):
    """ Parse the  line node to get the name of the line """
    id_node = l.getElementsByTagName("ept:lineName")[0]
    return id_node.firstChild.data
