import fnmatch
import hashlib
import os
import pathlib
from typing import List, Set

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


def _get_excluded_dirs() -> Set[str]:
    exlusion_list_config_file = ".pieignore"
    excluded_dirs = {pathlib.PosixPath(os.getcwd(), file) for file in [".git", "__pycache__"]}
    if not os.path.exists(exlusion_list_config_file):
        return excluded_dirs
    with open(exlusion_list_config_file, "r") as file:
        lines = file.readlines()
        excluded_dirs.update({pathlib.PosixPath(os.getcwd(), line.replace("\n", "")) for line in lines})
    return excluded_dirs


def get_py_files_in_dirs(dirs: List[str]):
    files = []
    if not dirs:
        return files
    excl = _get_excluded_dirs()
    for dir in dirs:
        for dirpath, _, filenames in os.walk(dir):
            filenames = fnmatch.filter(filenames, "*.py")
            files.extend(
                [
                    pathlib.PosixPath(dirpath, f_name) for f_name in filenames
                    if pathlib.PosixPath(dirpath, f_name).parent not in excl
                ]
            )
    return files
