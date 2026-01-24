import os
import sys
import subprocess
from pathlib import Path

def open_file(filename: str):
    path = Path(filename).resolve()

    if not path.exists():
        return

    if sys.platform.startswith("linux"):
        subprocess.Popen(["xdg-open", str(path)])
    elif sys.platform == "darwin":
        subprocess.Popen(["open", str(path)])
    elif sys.platform == "win32":
        os.startfile(path)
