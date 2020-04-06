import json
import math
import re

import numpy as np
from pyproj import Proj, transform

# Constants
EPSG_OUT = 'epsg:4326'
EPSG_IN = 'epsg:23030'
LINE_FORWARD_DIRECTION = 'FORWARD'
LINE_RETURN_DIRECTION = 'BACKWARD'
LINE_FORWARD_DIRECTION_CODE = '1'
LINE_RETURN_DIRECTION_CODE = '2'
LINE_NAME_SEPARATOR = '-'
WORKING_DAY_CODE = "1"
SATURDAY_DAY_CODE = "2"
SUNDAY_DAY_CODE = "3"


class Line():
    """ Entity representing a transport Line """

    def __init__(self, id, name, direction):
        self.id = str(id)
        self.name = name
        self.direction = direction
        if LINE_NAME_SEPARATOR in self.name:
            parts = self.name.split(LINE_NAME_SEPARATOR)
            self.origin = parts[0].strip()
            self.destination = parts[2].strip() if len(parts) == 3 \
                else parts[1].strip()

    # Array of stops
    stops = []

    # origin name
    origin = ''

    # destination name
    destination = ''

    # route expressed as a array of Locations
    route = []

    def get_client_line_id(self):
        return ("I" if self.direction == LINE_FORWARD_DIRECTION else "V") + self.id

    def get_agency_direction_name(self):
        return "IDA" if self.direction == LINE_FORWARD_DIRECTION else "VLT"

    def get_agency_direction_code(self):
        return LINE_FORWARD_DIRECTION_CODE if self.direction == LINE_FORWARD_DIRECTION else LINE_RETURN_DIRECTION_CODE

    def get_reverse_name(self):
        result = self.name
        if LINE_NAME_SEPARATOR in self.name:
            parts = self.name.split(LINE_NAME_SEPARATOR)
            name = ''
            for i in range(len(parts)):
                name += parts[(len(parts) - 1) - i].strip()
                if i < (len(parts) - 1):
                    name += " - "
            result = name.strip()
        return result

    def get_origin_name(self):
        return self.origin

    def get_destination_name(self):
        return self.destination

    def get_line_request_unique_code(self):
        return self.id + self.get_agency_direction_name()

    def set_stops(self, stops):
        self.stops = stops

    def set_route(self, route):
        self.route = route

    def is_night_line(self):
        return re.match("([Gg])\\d", self.id) is not None

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.direction == other.direction

    def __unicode__(self):
        return self.id

    def to_dict(self):
        """ Converts the object into a dictionary used for serializing """
        result = {'Id': self.get_client_line_id(), 'AgencyId': self.id, 'Name': self.name.upper(),
                  'Dir': self.direction, 'Night': self.is_night_line(),
                  'Stops': [s.to_dict() for s in self.stops],
                  'Map': [l.to_dict() for l in self.route]}
        return result


class Schedule(object):
    """ Class representing the schedule to a stop."""

    def __init__(self, working_times_list, saturday_times_list, sunday_times_list):
        self.working = working_times_list
        self.saturday = saturday_times_list
        self.sunday = sunday_times_list

    def __eq__(self, other):
        return self.working == other.working and self.saturday == other.saturday and \
               self.sunday == other.sunday

    def to_dict(self):
        return {'Wor': ",".join(self.working), 'Sat': ",".join(self.saturday), 'Sun': ",".join(self.sunday)}


class Stop():
    """ Entity representing a Stop """

    def __init__(self, id, name, location):
        self.id = id
        self.name = name
        self.location = location

    connections = []  # Array of connections
    schedule = Schedule([], [], [])

    def update_location(self, location):
        self.location = location

    def set_connections(self, connections):
        self.connections = connections

    def connections_to_string(self):
        return " ".join(self.connections)

    def to_dict(self):
        """ Converts the object into a dictionary used for serializing """
        result = {'Id': self.id, 'Na': self.name, 'Co': self.connections_to_string(), \
                  'Lc': self.location.to_dict(), 'Sc': self.schedule.to_dict()}
        return result

    def __unicode__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and \
               self.location == other.location and self.schedule == other.schedule


class Location(object):
    """ Entity representing a location expressed in latitude and longitude."""

    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

    def __eq__(self, other):
        return math.isclose(self.lat, other.lat, abs_tol=0.0001) and \
               math.isclose(self.long, other.long, abs_tol=0.0001)

    @classmethod
    def from_coordinates(cls, x, y):
        long, lat = transform(Proj(init=EPSG_IN), Proj(init=EPSG_OUT), x, y)
        return cls(lat, long)

    def to_dict(self):
        return {'La': self.lat, 'Lo': self.long}


def coordinates_to_locations(coordinates):
    """ Receives a matrix of coordinates and transforms it into a list of Locations """
    np_coords = np.array(coordinates)
    longs, lats = transform(Proj(init=EPSG_IN), Proj(init=EPSG_OUT), np_coords[:, 0], np_coords[:, 1])
    length = len(lats)
    result = []
    for i in range(length):
        result.append(Location(lats[i], longs[i]))
    return result
