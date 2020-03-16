import os
from broker.core import get_all_lines


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
    get_all_lines()

if __name__ == "__main__":
    main()
