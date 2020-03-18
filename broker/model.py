import json


LINE_FORWARD_DIRECTION = 'FORWARD'
LINE_RETURN_DIRECTION = 'BACKWARD'
LINE_NAME_SEPARATOR = '-'

"""
    Entity representing a transport Line
"""
class Line ():
    def __init__(self, id, name, direction):
        self.id = id
        self.name = name
        self.direction = direction
        if LINE_NAME_SEPARATOR in self.name:
            parts = self.name.split(LINE_NAME_SEPARATOR)
            self.origin = parts[0].strip()
            self.destination = parts[2].strip() if len(parts) == 3 \
                else parts[1].strip()

    # list of stops
    stops = []

    # origin name
    origin = ''

    # destination name
    destination = ''

    def get_agency_direction(self):
        return "IDA" if self.direction==LINE_FORWARD_DIRECTION else "VLT"

    def get_origin_name (self):
        return self.origin

    def get_destination_name (self):
        return self.destination

    def get_line_request_unique_code (self):
        return self.id + self.get_agency_direction()

    def set_stops (self, stops):
        self.stops = stops

    def to_json(self, pretty=True):
        data = {'AgencyId': self.id, 'Name': self.name, 'Dir': self.direction, 'Stops': [s.to_json(True) for s in self.stops]}
        return json.dumps(data, indent=(4 if pretty else None), ensure_ascii=False)

    def __unicode__(self):
        return self.id


"""
    Entity representing a Stop
"""
class Stop ():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_json(self, pretty=False):
        data = {'id': self.id, 'name': self.name }
        return json.dumps(data, indent=(4 if pretty else None), ensure_ascii=False)

    def __unicode__(self):
        return self.id