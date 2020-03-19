import unittest

from broker.model import Line, LINE_FORWARD_DIRECTION

"""
    Test suite of Line class
"""
class TestLine(unittest.TestCase):
    def test_origin_regularLineName(self):
        # Given
        l = Line(66, "PLACE1 - PLACE2",LINE_FORWARD_DIRECTION)
        # When
        origin = l.get_origin_name()
        # Then
        self.assertEqual(origin, "PLACE1", "Origin is not correct")

    def test_destination_regularLineName(self):
        # Given
        l = Line(66, "PLACE1 - PLACE2",LINE_FORWARD_DIRECTION)
        # When
        dest = l.get_destination_name()
        # Then
        self.assertEqual(dest, "PLACE2", "Destination is not correct")


if __name__ == '__main__':
    unittest.main()
