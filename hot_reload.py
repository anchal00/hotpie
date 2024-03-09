import os
import subprocess
import sys
import threading
import time

from utils import calculate_sha256_hash, get_py_files_in_dir


class HotReloadWatchDog(threading.Thread):

    _process = None
    _module = None

    def __init__(self, py_module) -> None:
        threading.Thread.__init__(self)
        self._module = py_module

    def _spawn_process(self):
        if self._process is not None and self._process.poll() is None:
            print("Reloading.....")
            self._process.kill()
            self._process.wait()
        self._process = subprocess.Popen(args=[sys.executable, self._module])
        print(f"Spawned new process with pid {self._process.pid}")

    def watch(self):
        file_hash_dict = {}
        dir = os.getcwd()
        print(f"Hot Reload: Watching files under dir {dir}")
        while True:
            files = get_py_files_in_dir(dir)
            for file in files:
                if file == "hot_reload.py":
                    continue
                new_hash = calculate_sha256_hash(file)
                old_hash = file_hash_dict.get(file)
                if not old_hash:
                    file_hash_dict[file] = new_hash
                elif old_hash != new_hash:
                    file_hash_dict[file] = new_hash
                    print(f"File {file} changed !")
                    self._spawn_process()
            time.sleep(1)

    def run(self) -> None:
        self._spawn_process()
        self.watch()
