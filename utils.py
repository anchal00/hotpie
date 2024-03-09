import fnmatch
import hashlib
import os


def calculate_sha256_hash(filename):
    hash = hashlib.sha256()
    bytarray = bytearray(128*1024)
    mv = memoryview(bytarray)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            hash.update(mv[:n])
    return hash.hexdigest()


def get_py_files_in_dir(dir):
    files = []
    for *_, filenames in os.walk(dir):
        filenames = fnmatch.filter(filenames, "*.py")
        files.extend(filenames)
    return files
