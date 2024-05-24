import os
import subprocess
import sys

# Dictionary of packages to install, mapping module names to their respective package names
packages = {"whisper": "openai-whisper"}
for module_name, package_name in packages.items():
    try:
        __import__(module_name)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
