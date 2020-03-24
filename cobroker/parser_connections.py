import json
import re


def extract_lines(lines_time_json, line_id):
    """ Extracts the lines from the next-transport-time information """
    lines = []
    line_items = json.loads(lines_time_json.replace("'", "\""))
    for l in line_items:
        id = l["Linea"]
        line = re.match("L?(.{1,2})", id)
        assert line is not None, f"Unrecognized line id format in connections: {id}"
        if line.group(1) not in lines and line.group(1) != line_id:
            lines.append(line.group(1))
    return lines


def parse_connections(response, line_id):
    """ Parse json response containing the stops of a line and returns dict with connections per stop """
    data = json.loads(response)
    stops = data["features"]
    result = {}
    for i in range(len(stops)):
        stop_id = stops[i]["properties"]["ParadaAutobus"]
        lines = extract_lines(stops[i]["properties"]["tiempos"], line_id)
        result[stop_id] = lines
    return result
