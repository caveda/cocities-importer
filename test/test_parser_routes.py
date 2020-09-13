import unittest

from cobroker.model import Line, LINE_FORWARD_DIRECTION, Location, Stop
from cobroker.parser_routes import parse_route

TEST_JSON_RESPONSE = """{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": "666759",
            "geometry": {
                "type": "MultiLineString",
                "coordinates": [
                    [
                        [
                            506233.065172259,
                            4790795.30995913
                        ],
                        [
                            505959.0574198989,
                            4790065.031728711
                        ]
                    ]
                ]
            }
        }
    ],
    "totalFeatures": 1
}"""


class TestParserRoutes(unittest.TestCase):
    """ Test suite of parser_routes """

    def test_parse_routes_validJSON_returnedExpectedRoute(self):
        # Given
        input_json = TEST_JSON_RESPONSE
        expected_route = [Location.from_coordinates(506233.065172259, 4790795.30995913),
                          Location.from_coordinates(505959.0574198989, 4790065.031728711)]
        line = Line(66, "PLACE1 - Place2", LINE_FORWARD_DIRECTION)
        location1001 = Location.from_coordinates(506233.065172259, 4790795.30995913)
        location1001.set_raw_coordinates_simplified(506233, 4790795)
        location1002 = Location.from_coordinates(505959.0574198989, 4790065.031728711)
        location1002.set_raw_coordinates_simplified(505959, 4790065)
        line.stops = [Stop("1001", "Stop name 1", location1001),
                      Stop("1002", "Stop name 2", location1002)]
        # When
        route = parse_route(line, input_json)
        # Then
        self.assertListEqual(route, expected_route)


if __name__ == '__main__':
    unittest.main()
