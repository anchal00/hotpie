import fnmatch
import hashlib
import os
import pathlib

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


def get_py_files_in_dirs(dirs):
    files = []
    if not dirs:
        return files
    for dir in dirs:
        for dirpath, subdirs, filenames in os.walk(dir):
            filenames = fnmatch.filter(filenames, "*.py")
            files.extend(
                [pathlib.PosixPath(dirpath, filename) for filename in filenames]
            )
            subdirs = list(filter(lambda subdir: subdir in [".git", "__pycache__"], subdirs))
            py_files_in_subdirs = get_py_files_in_dirs(subdirs)
            if py_files_in_subdirs:
                files.extend([pathlib.PosixPath(dirpath, path) for path in py_files_in_subdirs])
    return files
