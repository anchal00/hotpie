
import os
import pathlib
from typing import List, Union


class HotpieConfig:
    _config = None
    _module = None
    _ext = ".py"
    _dirs = None

    def __init__(self, main_module: str, watch_dirs: List[str] = None, watch_interval_secs: int = 1) -> None:
        root_dir = os.getcwd()
        self._dirs = [root_dir]
        if watch_dirs:
            # Look for changes in files in other dirs apart from current dir
            assert (os.path.exists(dir) is True for dir in watch_dirs)
            self._dirs.extend(watch_dirs)
        py_module = f"{main_module}{self._ext}"
        py_module_abs_path = pathlib.PosixPath(root_dir, py_module)
        assert os.path.exists(py_module_abs_path)
        self._module = py_module_abs_path
        self._interval = watch_interval_secs

    @property
    def module(self) -> pathlib.PosixPath:
        return self._module

    @property
    def dirs(self) -> List[Union[pathlib.PosixPath, str]]:
        return self._dirs

    @property
    def watch_interval(self) -> int:
        return self._interval


config = HotpieConfig
