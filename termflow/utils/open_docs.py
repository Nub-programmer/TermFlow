import os
import sys
import subprocess
from pathlib import Path
from termflow.utils.resources import get_resource_path

def open_file(filename: str):
    path = get_resource_path(filename)

    if not path.exists():
        return

    if sys.platform.startswith("linux"):
        subprocess.Popen(["xdg-open", str(path)])
    elif sys.platform == "darwin":
        subprocess.Popen(["open", str(path)])
    elif sys.platform == "win32":
        os.startfile(path)
