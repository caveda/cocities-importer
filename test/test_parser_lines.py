import unittest

from broker.model import Line, LINE_FORWARD_DIRECTION
from broker.parser_lines import parse_lines

TEST_XML_RESPONSE = """<Collection xsi:schemaLocation="http://namespace.emotion-project.eu/version/Final2.1.0/pubtrans https://www.blabla.eus/wfsCocities/schemas/CoCities-Data-GML-Final2.2.0/eMotion/eMotionVersionFinal2.1.0-PublicTransport.xsd http://www.opengis.net/wfs https://www.blabla.com/wfsCocities/schemas/wfs/1.1.0/wfs.xsd" xmlns:wfs="http://www.opengis.net/wfs" xmlns:edi="http://namespace.emotion-project.eu/version/Final2.1.0/dir" xmlns:ogc="http://www.opengis.net/ogc" xmlns:eti="http://namespace.emotion-project.eu/version/Final2.1.0/trinfo" xmlns:elr="http://namespace.emotion-project.eu/version/Final2.1.0/locref" xmlns:ect="http://namespace.emotion-project.eu/version/Final2.1.0/ctypes" xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:enw="http://namespace.emotion-project.eu/version/Final2.1.0/net" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:bnw="http://co-cities.bilbokoudala.net/version/2.2.0/net" xmlns:ept="http://namespace.emotion-project.eu/version/Final2.1.0/pubtrans" xmlns:ows="http://www.opengis.net/ows" xmlns:gml="http://www.opengis.net/gml" xmlns:xlink="http://www.w3.org/1999/xlink">  
    <ept:Line gml:id="1001">
         <ept:identity>
            <ept:LineCode>
               <ept:identifier>1001</ept:identifier>
            </ept:LineCode>
         </ept:identity>
         <ept:lineName>Origin1 - Destination1</ept:lineName>
         <ept:routesForLine>
            <ept:Route>
               <ept:identity>
                  <ept:RouteCode>
                     <ept:identifier>189</ept:identifier>
                  </ept:RouteCode>
               </ept:identity>
               <ept:routeName>1001_FOR</ept:routeName>
               <ept:direction>
                  <ept:Direction>
                     <ept:identity>
                        <ept:DirectionCode>
                           <ept:identifier>IDA</ept:identifier>
                        </ept:DirectionCode>
                     </ept:identity>
                  </ept:Direction>
               </ept:direction>
            </ept:Route>
         </ept:routesForLine>
         <ept:routesForLine>
            <ept:Route>
               <ept:identity>
                  <ept:RouteCode>
                     <ept:identifier>1A289</ept:identifier>
                  </ept:RouteCode>
               </ept:identity>
               <ept:routeName>1001_VLT</ept:routeName>
               <ept:direction>
                  <ept:Direction>
                     <ept:identity>
                        <ept:DirectionCode>
                           <ept:identifier>VLT</ept:identifier>
                        </ept:DirectionCode>
                     </ept:identity>
                  </ept:Direction>
               </ept:direction>
            </ept:Route>
         </ept:routesForLine>
      </ept:Line>
       <ept:Line gml:id="1002">
         <ept:identity>
            <ept:LineCode>
               <ept:identifier>1002</ept:identifier>
            </ept:LineCode>
         </ept:identity>
         <ept:lineName>Origin2 - Middle2 - Destination2/Alt2</ept:lineName>
         <ept:routesForLine>
            <ept:Route>
               <ept:identity>
                  <ept:RouteCode>
                     <ept:identifier>14489</ept:identifier>
                  </ept:RouteCode>
               </ept:identity>
               <ept:routeName>1002_FOR</ept:routeName>
               <ept:direction>
                  <ept:Direction>
                     <ept:identity>
                        <ept:DirectionCode>
                           <ept:identifier>IDA</ept:identifier>
                        </ept:DirectionCode>
                     </ept:identity>
                  </ept:Direction>
               </ept:direction>
            </ept:Route>
         </ept:routesForLine>
         <ept:routesForLine>
            <ept:Route>
               <ept:identity>
                  <ept:RouteCode>
                     <ept:identifier>211</ept:identifier>
                  </ept:RouteCode>
               </ept:identity>
               <ept:routeName>1002_VLT</ept:routeName>
               <ept:direction>
                  <ept:Direction>
                     <ept:identity>
                        <ept:DirectionCode>
                           <ept:identifier>VLT</ept:identifier>
                        </ept:DirectionCode>
                     </ept:identity>
                  </ept:Direction>
               </ept:direction>
            </ept:Route>
         </ept:routesForLine>
      </ept:Line>
      </Collection>"""

"""
    Test suite of Stop class
"""


class TestParserLines(unittest.TestCase):
    def test_parse_lines_validXML_linesReturnedExpected(self):
        # Given
        input_xml = TEST_XML_RESPONSE
        # When
        lines = parse_lines(input_xml)
        # Then
        expected_lines = [Line('1001', "Origin1 - Destination1", LINE_FORWARD_DIRECTION),
                          Line('1002', "Origin2 - Middle2 - Destination2/Alt2", LINE_FORWARD_DIRECTION)]
        self.assertListEqual(lines, expected_lines)


if __name__ == '__main__':
    unittest.main()
