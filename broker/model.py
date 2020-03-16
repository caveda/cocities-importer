import json


LINE_FORWARD_DIRECTION = 'FORWARD'
LINE_RETURN_DIRECTION = 'BACKWARD'

"""
    Object representing a transport Line
"""
class Line ():
    def __init__(self, id, name, direction):
        self.id = id
        self.name = name
        self.direction = direction

    def get_line_code (self):
        return self.id + self.direction

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