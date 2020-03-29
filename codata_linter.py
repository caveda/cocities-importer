
def sanitize (lines):
    """ Receives a list of lines, removes the faulty ones and returns a sanitized copy. """
    return filter(lambda line: len(line.stops) > 0, lines)
