def sanitize(lines):
    """ Receives a list of lines, removes the faulty ones and returns a sanitized copy. """
    filtered_lines = remove_lines_without_stops(lines)
    return sort_lines_by_id(filtered_lines)


def sort_lines_by_id(lines):
    return sorted(lines, key=lambda line: line.id)


def remove_lines_without_stops(lines):
    return filter(lambda line: len(line.stops) > 0, lines)
