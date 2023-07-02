import hashlib


def hash_data(value):
    return hashlib.sha256(str(value).encode('utf-8')).hexdigest()
