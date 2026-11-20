#!/usr/bin/env python3
import os, platform, shutil
total, used, free = shutil.disk_usage(os.getcwd())
print(f"Python version: {platform.python_version()}")
print(f"Operating system: {platform.system()} {platform.release()}")
print(f"Current working directory: {os.getcwd()}")
print(f"Available disk space: {free} bytes ({free / (1024**3):.2f} GiB)")
