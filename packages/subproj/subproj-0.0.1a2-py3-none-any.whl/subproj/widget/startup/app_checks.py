import re
import shutil
import subprocess


def check_thg(self, result):
    if not shutil.which("thg"):
        result.append("Error: TortoiseHG not found.")
        self.log_append(result[-1])
    else:
        response = subprocess.run(["thg", "version"], capture_output=True)
        if not response.returncode == 0:
            result.append("Error: TortoiseHG not found.")
            self.log_append(result[-1])
        elif b"version 6.1" not in response.stdout:
            result.append("Warning: TortoiseHG version 6.1 not found.")
            self.log_append(result[-1])


def check_py(self, result):
    if not shutil.which("py"):
        result.append("Error: Python 3 not found.")
        self.log_append(result[-1])
    else:
        response = subprocess.run(["py", "-3", "-V"], capture_output=True)
        if not response.returncode == 0:
            result.append("Error: Python3 not found.")
            self.log_append(result[-1])
        elif b"Python 3.10" not in response.stdout:
            result.append("Warning: Python version 3.10 not found.")
            self.log_append(result[-1])


def check_git(self, result):
    if not shutil.which("git"):
        result.append("Error: git not found.")
        self.log_append(result[-1])
    else:
        response = subprocess.run(["git", "version"], capture_output=True)
        version_str = response.stdout.strip()
        version = re.split(rb".+?(\d+)+\.(\d+)\.(\d+).*", version_str)
        if not response.returncode == 0:
            result.append("Error: git not found.")
            self.log_append(result[-1])
        elif tuple(map(int, version[1:-1])) < (
            2,
            39,
            1,
        ):
            result.append("Warning: Git version 2.39.0 or newer not found.")
            self.log_append(result[-1])
