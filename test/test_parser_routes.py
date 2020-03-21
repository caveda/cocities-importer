import unittest

from cobroker.model import Line, LINE_FORWARD_DIRECTION, Location
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
                            506010.81625759,
                            4790061.66481957
                        ],
                        [
                            506007.93349353,
                            4790055.20073894
                        ],
                        [
                            506006.65353876,
                            4790054.01883834
                        ]
                    ]
                ]
            }
        }
    ]
}"""


class TestParserRoutes(unittest.TestCase):
    """ Test suite of parser_routes """

    def test_parse_routes_validJSON_returnedExpectedRoute(self):
        # Given
        input_json = TEST_JSON_RESPONSE
        # When
        route = parse_route(input_json)
        # Then
        expected_route = [Location.from_coordinates(506010.81625759,4790061.66481957),
                          Location.from_coordinates(506007.93349353, 4790055.20073894),
                          Location.from_coordinates(506006.65353876, 4790054.01883834)]
        self.assertListEqual(route, expected_route)


if __name__ == '__main__':
    unittest.main()
