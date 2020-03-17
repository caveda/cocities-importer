import json


LINE_FORWARD_DIRECTION = 'FORWARD'
LINE_RETURN_DIRECTION = 'BACKWARD'
LINE_NAME_SEPARATOR = '-'

"""
    Object representing a transport Line
"""
class Line ():
    def __init__(self, id, name, direction):
        self.id = id
        self.name = name
        self.origin = self.name.split(LINE_NAME_SEPARATOR)[0].strip()
        self.destination = self.name.split(LINE_NAME_SEPARATOR)[1].strip()
        self.direction = direction

    def get_agency_direction(self):
        return "IDA" if self.direction==LINE_FORWARD_DIRECTION else "VLT"

    def get_origin_name (self):
        return self.origin

    def get_destination_name (self):
        return self.destination

    def get_line_request_unique_code (self):
        return self.id + self.get_agency_direction()

    def json(self, pretty=False):
        data = {'AgencyId': self.id, 'Name': self.name, 'Dir': self.direction}
        return json.dumps(data, indent=(4 if pretty else None), ensure_ascii=False)

    def __unicode__(self):
        return self.id


"""
    Object representing a Stop of a Line
"""
class Stop ():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def json(self, pretty=False):
        data = {'id': self.id, 'name': self.name }
        return json.dumps(data, indent=(4 if pretty else None))

    def __unicode__(self):
        return self.id