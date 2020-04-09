import json
import re

from cobroker import cologger
from cobroker.model import Schedule, WORKING_DAY_CODE, SATURDAY_DAY_CODE, SUNDAY_DAY_CODE


def parse_schedule(response):
    """ Parse json response containing the schedule of a stop """
    data = json.loads(response)
    try:
        raw_schedules = data["RESPUESTA"]["LISTA"]["DETALLE"]
        schedule = digest_json_schedules(raw_schedules)
    except:
        # Some schedules are missing on the server
        schedule = Schedule([], [], [])
        cologger.log(f"Missing schedule")
    return schedule


def digest_json_schedules(json_schedules):
    """ Build schedule from json schedule data """
    result = dict()
    for s in json_schedules:
        day = s["TIPO_DIA"]
        new_value = sorted(result.get(day, []) + schedule_to_array(s["HORAS_SALIDA"]))
        result[day] = sanitize_schedule_times(new_value)
    return build_schedule(result)


def schedule_to_array(schedule):
    """ Parses schedule string looking for time items (e.g 12:30) and returns them as array. """
    matches = re.findall("\d\d:\d\d", schedule)
    assert len(matches) > 0, f"Unrecongnized schedule content: {schedule}"
    return matches


def build_schedule(result):
    """ Builds a Schedule object out of a dictionary """
    return Schedule(result.get(WORKING_DAY_CODE, []),
                    result.get(SATURDAY_DAY_CODE, []),
                    result.get(SUNDAY_DAY_CODE, []))


def sanitize_schedule_times(schedule):
    """ Some time comes in the wrong format, e.g. 26:11 which this function fixes and replaces by 02:11 """
    for i in range(len(schedule)):
        schedule[i] = schedule[i].replace("24:", "00:"). \
            replace("25:", "01:"). \
            replace("26:", "02:"). \
            replace("27:", "03:"). \
            replace("28:", "04:"). \
            replace("29:", "05:"). \
            replace("30:", "06:"). \
            replace("31:", "07:"). \
            replace("32:", "08:")
    return schedule
