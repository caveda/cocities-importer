import unittest

from cobroker.parser_connections import parse_connections

TEST_JSON_RESPONSE = """{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": "SFbus_Paradas.fid-6d676182_1710ccafab2_-7839",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    665435.95850965,
                    2221217.10272522
                ]
            },
            "geometry_name": "Geometry",
            "properties": {
                "idauto": 164225,
                "id": "8_5_1749_136",
                "lineIdPerm": 8,
                "routeIdPerm": 5,
                "journeyPatternIdPerm": 1749,
                "stopPointIdPerm": 136,
                "CodigoLinea": "11",
                "CODRUTA": 5,
                "LineaRuta": "66 - FFF",
                "RUTA": "Week/Place2",
                "RUTA_EU": "Week/Place2",
                "ParadaAutobus": "7011",
                "NombreParada": "Baker St",
                "NombreParada_EU": "Baker St",
                "rotation": -188.97,
                "locatingsystemname": "EPSG:23030",
                "Color": "#D39CA",
                "tiempos": "[ {'Linea':'L03', 'Tiempos': {'T1': 5,'T2': 16}}, {'Linea':'L28', 'Tiempos': {'T1': 4,'T2': 22}}, {'Linea':'L11', 'Tiempos': {'T1': 13,'T2': 43}}, {'Linea':'L22', 'Tiempos': {'T1': 25,'T2': 45}}, {'Linea':'L30', 'Tiempos': {'T1': 16,'T2': 32}}, {'Linea':'L72', 'Tiempos': {'T1': 14,'T2': 29}}, {'Linea':'L71', 'Tiempos': {'T1': 11,'T2': 30}}, {'Linea':'LH7', 'Tiempos': {'T1': 31,'T2': null}}, {'Linea':'L77', 'Tiempos': {'T1': 0,'T2': null}}, {'Linea':'K8', 'Tiempos': {'T1': 17,'T2': null}}, {'Linea':'F4', 'Tiempos': {'T1': 4,'T2': null}}, {'Linea':'F2', 'Tiempos': {'T1': 19,'T2': null}}]"
            }
        },
        {
            "type": "Feature",
            "id": "SFbus_Paradas.fid-6d676182_1710ccafab2_-7838",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    506356.18644944,
                    4789946.85557823
                ]
            },
            "geometry_name": "Geometry",
            "properties": {
                "idauto": 164226,
                "id": "8_5_1749_138",
                "lineIdPerm": 8,
                "routeIdPerm": 5,
                "journeyPatternIdPerm": 1749,
                "stopPointIdPerm": 138,
                "CodigoLinea": "11",
                "CODRUTA": 5,
                "LineaRuta": "66 - FFF",
                "RUTA": "Week/Place2",
                "RUTA_EU": "Week/Place2",
                "ParadaAutobus": "9012",
                "NombreParada": "High St",
                "NombreParada_EU": "High St",
                "rotation": -158.47,
                "locatingsystemname": "EPSG:23030",
                "Color": "#D39CA",
                "tiempos": "[ {'Linea':'L11', 'Tiempos': {'T1': 14,'T2': 44}}, {'Linea':'L22', 'Tiempos': {'T1': 0,'T2': 27}}, {'Linea':'H8', 'Tiempos': {'T1': 6,'T2': null}}, {'Linea':'LH8', 'Tiempos': {'T1': 0,'T2': null}}, {'Linea':'LF9', 'Tiempos': {'T1': 33,'T2': 33}}]"
            }
        }]}"""


class TestParserConnections(unittest.TestCase):
    """ Test suite of parser_connections """

    def test_parse_connections_validJSON_returnedExpectedConnectionsPerStop(self):
        # Given
        input_json = TEST_JSON_RESPONSE
        # When
        connections = parse_connections(input_json,"11")
        # Then
        expected_connections = {'7011': ['03', '28', '22', '30', '72', '71', 'H7', '77', 'K8', 'F4', 'F2'],
                                '9012': ['22', 'H8', 'F9']}
        self.assertDictEqual(connections, expected_connections)


if __name__ == '__main__':
    unittest.main()
