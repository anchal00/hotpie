import pathlib
import subprocess
import sys
import threading
import time
from typing import List

from hotpie_config import HotpieConfig
from utils import get_py_files_in_dirs, has_file_changed


class HotReloadWatchDog(threading.Thread):

    _process = None
    _module = None

    def __init__(self, config: HotpieConfig) -> None:
        threading.Thread.__init__(self)
        self._config = config

    def _spawn_process(self):
        if self._process is not None and self._process.poll() is None:
            self._process.kill()
            self._process.wait()
        self._process = subprocess.Popen(args=[sys.executable, self._config.module])
        print(f"Spawned new process with pid {self._process.pid}")

    def watch(self):
        dirs = self._config.dirs
        print(f"Hot Reload: Watching files under dir {dirs}")
        while True:
            files: List[pathlib.PosixPath] = get_py_files_in_dirs(dirs)
            for file in files:
                if str(file) == __file__:
                    continue
                if has_file_changed(file):
                    print(f"Changes detected in file {file}")
                    print("Reloading.....")
                    self._spawn_process()
            time.sleep(self._config.watch_interval)

    def run(self) -> None:
        self._spawn_process()
        self.watch()
