import sys
import hashlib


def calculate_hash (file):
    """ Calculates a hash (SHA256) of file """
    sha3 = hashlib.sha3_256()
    buffer_size = 65536
    with open(file, 'rb') as f:
        while True:
            chunk = f.read(buffer_size)
            if chunk:
                sha3.update(chunk)
            else:
                break
    return sha3.hexdigest()

