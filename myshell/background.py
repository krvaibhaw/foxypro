import subprocess
import shlex

def handle_background(command):
    
    parts = shlex.split(command)
    try:
        process = subprocess.Popen(parts)
        print(f"Started process {process.pid} in background")
    except FileNotFoundError:
        print(f"Command not found: {command}")
