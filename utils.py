import fnmatch
import hashlib
import os


_FILE_HASHES = {}


def _calculate_md5_hash(filename):
    hash = hashlib.md5()
    bytarray = bytearray(128*1024)
    mv = memoryview(bytarray)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            hash.update(mv[:n])
    return hash.hexdigest()


def has_file_changed(filename):
    new_hash = _calculate_md5_hash(filename)
    saved_hash = _FILE_HASHES.setdefault(filename, new_hash)
    if saved_hash != new_hash:
        _FILE_HASHES[filename] = new_hash
        return True
    return False


def get_py_files_in_dir(dir):
    files = []
    for *_, filenames in os.walk(dir):
        filenames = fnmatch.filter(filenames, "*.py")
        files.extend(filenames)
    return files
