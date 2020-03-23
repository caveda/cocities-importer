import unittest

from cobroker.model import Line, LINE_FORWARD_DIRECTION


class TestLine(unittest.TestCase):
    """ Test suite of Line class """

    def test_origin_regularLineName(self):
        # Given
        l = Line(66, "PLACE1 - PLACE2", LINE_FORWARD_DIRECTION)
        # When
        origin = l.get_origin_name()
        # Then
        self.assertEqual(origin, "PLACE1", "Origin is not correct")

    def test_destination_regularLineName(self):
        # Given
        l = Line(66, "PLACE1 - PLACE2", LINE_FORWARD_DIRECTION)
        # When
        dest = l.get_destination_name()
        # Then
        self.assertEqual(dest, "PLACE2", "Destination is not correct")

    def test_reverse_name_returnedNameReversed(self):
        # Given
        cases = [(Line(66, "PLACE1 - Place2", LINE_FORWARD_DIRECTION),"Place2 - PLACE1"),
                 (Line(66, "PLACE1 - PLACE2/PLACE3", LINE_FORWARD_DIRECTION),"PLACE2/PLACE3 - PLACE1"),
                 (Line(66, "PLACE1 - Place2 - PLACE3", LINE_FORWARD_DIRECTION),"PLACE3 - Place2 - PLACE1"),
                 (Line(66, "PLACE1 VERY LONG", LINE_FORWARD_DIRECTION),"PLACE1 VERY LONG"),
                 (Line(66, "PLACE1 - Place 2 long", LINE_FORWARD_DIRECTION),"Place 2 long - PLACE1"),
                 (Line(66, "Place 1 long - Place2", LINE_FORWARD_DIRECTION),"Place2 - Place 1 long")]
        for c in cases:
            # When
            reverse = c[0].get_reverse_name()
            # Then
            self.assertEqual(reverse, c[1])


if __name__ == '__main__':
    unittest.main()
