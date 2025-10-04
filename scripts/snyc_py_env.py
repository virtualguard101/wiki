#!/usr/bin/env python3

import os
import sys
import subprocess

def sync_py_env():
    """Sync Python environment from uv env to requirements.txt
    """
    subprocess.run(["rm", "-f", "requirements.txt"])
    subprocess.run("uv pip freeze > requirements.txt", shell=True, check=True)

if __name__ == "__main__":
    sync_py_env()
