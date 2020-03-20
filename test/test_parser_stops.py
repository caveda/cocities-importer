import unittest

from broker.model import Location, Stop, Line, LINE_FORWARD_DIRECTION
from broker.parser_stops import parse_stops

TEST_XML_RESPONSE = """<valores xmlns=""><![CDATA[<?xml version="1.0" encoding="UTF-8"?><data><other>Generic data</other><list>
       <DETALLE>
            <id>66</id>
            <NOMBRE>DestinationX</NOMBRE>
            <PARADAAUTOBUS>1001</PARADAAUTOBUS>
            <NOMBREPARADA>Stop name 1</NOMBREPARADA>
            <GEOMETRY_XLO>506233.065172259</GEOMETRY_XLO>
            <GEOMETRY_YLO>4790795.30995913</GEOMETRY_YLO>
        </DETALLE>
        <DETALLE>
            <CODIGOLINEA>66</CODIGOLINEA>
            <NOMBRE>DestinationX</NOMBRE>
            <PARADAAUTOBUS>1002</PARADAAUTOBUS>
            <NOMBREPARADA>Stop name 2</NOMBREPARADA>
            <GEOMETRY_XLO>505959.0574198989</GEOMETRY_XLO>
            <GEOMETRY_YLO>4790065.031728711</GEOMETRY_YLO>
        </DETALLE>
            <DETALLE>
            <CODIGOLINEA>66</CODIGOLINEA>
            <NOMBRE>Origin</NOMBRE>
            <PARADAAUTOBUS>1003</PARADAAUTOBUS>
            <NOMBREPARADA>Stop name 3</NOMBREPARADA>
            <GEOMETRY_XLO>506729.090865163</GEOMETRY_XLO>
            <GEOMETRY_YLO>4790445.69997587</GEOMETRY_YLO>
        </DETALLE></list></data>]]></valores>"""

"""
    Test suite of Stop class
"""
class TestParserStops(unittest.TestCase):
    def test_parse_stops_validXML_stopsReturnedExpected(self):
        # Given
        input_xml = TEST_XML_RESPONSE
        line = Line(66, "Origin - DestinationX",LINE_FORWARD_DIRECTION)
        # When
        stops = parse_stops(input_xml, line)
        # Then
        expected_stops = [Stop("1001", "Stop name 1", Location(43.26806999978483,-2.9245073992073762)),
                          Stop("1002", "Stop name 2", Location(43.26149629243633,-2.9278916590650783))]
        self.assertListEqual(stops, expected_stops)

if __name__ == '__main__':
    unittest.main()
