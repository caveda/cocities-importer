import unittest

from cobroker import core
from cobroker.model import Line, LINE_FORWARD_DIRECTION, Stop, Location


class TestCore(unittest.TestCase):
    """ Test suite of core """

    def test_add_stops_connections_from_cache_validDict_returnedConnectionsOk(self):
        # Given
        connections_cache = {"1234": ["I01", "I02", "V03"], "5678": ["I01", "I33"], "9012": ["V01"]}
        l = Line("01", "PLACE1 - PLACE2", LINE_FORWARD_DIRECTION)
        dummy_location = Location("10", "10")
        l.set_stops([Stop("1234", "Stop1", dummy_location),
                     Stop("5678", "Stop2", dummy_location),
                     Stop("9012", "Stop3", dummy_location)])
        # When
        core.add_stops_connections_from_cache(l, connections_cache)
        # Then
        expected_connections = {"1234": ["I02", "V03"], "5678": ["I33"], "9012": []}
        for s in l.stops:
            self.assertListEqual(s.connections, expected_connections[s.id])

    def test_get_stops_points_returnedStopsLocations(self):
        # Given
        l = Line("01", "PLACE1 - PLACE2", LINE_FORWARD_DIRECTION)
        l.set_stops([Stop("1234", "Stop1", Location(22.1, 3.1)),
                     Stop("5678", "Stop2", Location(22.4, 3.2)),
                     Stop("9012", "Stop3", Location(22.7, 3.3))])
        # When
        locations = core.get_stops_points(l)
        # Then
        expected_locations = [Location(22.1, 3.1), Location(22.4, 3.2), Location(22.7, 3.3)]
        self.assertListEqual(locations, expected_locations)


if __name__ == '__main__':
    unittest.main()
