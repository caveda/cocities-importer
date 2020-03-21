
from xml.dom import minidom
from broker.model import LINE_FORWARD_DIRECTION, Line


"""
  Parse the response of all lines query
"""
def parse_lines (xml_response):
    xmldoc = minidom.parseString(xml_response)
    lines_nodes = xmldoc.getElementsByTagName("ept:Line")
    result =[]
    for l in lines_nodes:
        line = Line(parse_line_id(l), parse_line_name(l), LINE_FORWARD_DIRECTION)
        result.append(line)
    return result

"""
    Parse a line node to get the line ID
"""
def parse_line_id(l):
    id_node = l.getElementsByTagName("ept:LineCode")[0].getElementsByTagName("ept:identifier")
    return id_node[0].firstChild.data


"""
    Parse the  line node to get the name of the line∫
"""
def parse_line_name(l):
    id_node = l.getElementsByTagName("ept:lineName")[0]
    return id_node.firstChild.data

