import unittest

from cobroker.model import Location, Stop, Schedule
from cobroker.parser_schedule import parse_schedule

TEST_JSON_RESPONSE = """{"RESPUESTA": {
 "DATOSGENERICOS": {
  "RETORNO": true,
  "MENSAJE": true
 },
 "LISTA": {"DETALLE": [
  {
   "HORAS_SALIDA": "07:0008:0009:0010:0011:0012:00",
   "COD_SENTIDO": "1",
   "TIPO_DIA": "1"
  },
  {
   "HORAS_SALIDA": "06:1507:1508:1509:1510:1511:1512:15",
   "COD_SENTIDO": "1",
   "TIPO_DIA": "1"
  },
  {
   "HORAS_SALIDA": "06:3007:3008:3009:3010:3011:3012:30",
   "COD_SENTIDO": "1",
   "TIPO_DIA": "1"
  },
  {
   "HORAS_SALIDA": "06:4507:4508:4509:4510:4511:4512:45",
   "COD_SENTIDO": "1",
   "TIPO_DIA": "1"
  },
  {
   "HORAS_SALIDA": "07:0008:0009:0010:0011:0012:00",
   "COD_SENTIDO": "1",
   "TIPO_DIA": "2"
  },
  {
   "HORAS_SALIDA": "06:3007:3008:3009:3010:3011:3012:30",
   "COD_SENTIDO": "1",
   "TIPO_DIA": "2"
  },
  {
   "HORAS_SALIDA": "08:0009:0010:0011:0012:00",
   "COD_SENTIDO": "1",
   "TIPO_DIA": "3"
  },
  {
   "HORAS_SALIDA": "07:3008:3009:3010:3011:3012:30",
   "COD_SENTIDO": "1",
   "TIPO_DIA": "3"
  }
 ]}
}}"""


class TestParserSchedule(unittest.TestCase):
    """ Test suite of parser_schedule """

    def test_parse_routes_validJSON_returnedExpectedSchedule(self):
        # Given
        input_json = TEST_JSON_RESPONSE
        stop = Stop("0999","Place St", Location("11", "2"))
        # When
        stop.schedule = parse_schedule(input_json)
        # Then
        expected_schedule = Schedule(["06:15","06:30","06:45","07:00","07:15","07:30","07:45","08:00","08:15","08:30","08:45","09:00","09:15","09:30","09:45","10:00","10:15","10:30","10:45","11:00","11:15","11:30","11:45","12:00","12:15","12:30","12:45"],
                                    ["06:30","07:00","07:30","08:00","08:30","09:00","09:30","10:00","10:30","11:00","11:30", "12:00","12:30"],
                                    ["07:30","08:00","08:30","09:00","09:30","10:00","10:30","11:00","11:30","12:00","12:30"])
        self.assertTrue(stop.schedule == expected_schedule)


if __name__ == '__main__':
    unittest.main()
