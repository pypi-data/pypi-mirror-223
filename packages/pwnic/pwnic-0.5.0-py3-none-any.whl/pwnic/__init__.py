"""Awesome `pwnic` is a Python cli/package created with https://github.com/TezRomacH/python-package-template"""

import sys
import time
from importlib import metadata as importlib_metadata
from pathlib import Path

from pwnic.exploits import load_exploit


def get_version() -> str:
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()

if sys.prefix == sys.base_prefix:
    print(
        "Your are not running inside a virtual environment! Be careful as this application might install other packages with pip"
    )
    time.sleep(5)

try:
    for type_dir in Path("exploits").iterdir():
        for exploit_dir in type_dir.iterdir():
            path = Path(exploit_dir)
            print(path)

            load_exploit(type=type_dir.stem, name=exploit_dir.stem)
except FileNotFoundError:
    pass
