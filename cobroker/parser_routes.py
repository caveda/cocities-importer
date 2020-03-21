import json


"""
  Parse json response containing the route of the line
"""
def parse_route (response):
    parsed_json = json.loads(response)
    result =[]
    for l in lines_nodes:
        line = Line(parse_line_id(l), parse_line_name(l), LINE_FORWARD_DIRECTION)
        result.append(line)
    return result

