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
    lines = fetch_transport_data()
    for l in lines:
        print (l.to_json())


def fetch_transport_data():
    lines = core.get_all_lines()
    for l in lines:
        l.set_stops(core.get_line_stops(l))
    return lines


if __name__ == "__main__":
    main()
