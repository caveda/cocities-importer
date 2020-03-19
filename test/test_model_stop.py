import unittest

from broker.model import Location, Stop

"""
    Test suite of Stop class
"""
class TestStop(unittest.TestCase):
    def test_location_locationExpected(self):
        # Given
        location = Location.from_coordinates(505478.21390717285,4790199.217272087)
        # When
        s = Stop("65422", "Some name",location)
        # Then
        self.assertEqual(s.location.lat, 43.26270820473875)
        self.assertEqual(s.location.long, -2.933814830041445)

if __name__ == '__main__':
    unittest.main()
