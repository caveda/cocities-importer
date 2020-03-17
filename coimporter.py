import os

from broker import core


"""
    Set environment variables
"""
def set_environment():
    with open('setupenv.sh') as f:
        processed = f.read().replace('export ', '')
    for line in processed.splitlines():
        var, _, value = line.partition('=')
        os.environ[var] = value.replace('"','')

"""
    Main function
"""
def main():
    set_environment()
    lines = core.get_all_lines()
    for l in lines:
        l.stops = core.get_line_stops (l)


if __name__ == "__main__":
    main()
