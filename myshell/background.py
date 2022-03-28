import subprocess
import shlex

def handle_background(command):
    parts = shlex.split(command)
    process = subprocess.Popen(parts)
    print(f"Started process {process.pid} in background")
