from importlib.util import find_spec
import sys
import subprocess

def ensure_package_installed(package_name):
    if not find_spec(package_name):
        print(f"{package_name} not found, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])