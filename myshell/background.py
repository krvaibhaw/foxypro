import subprocess

def handle_background(command):
    try:
        process = subprocess.Popen(command, shell=True)
        print(f"Started process {process.pid} in background")
    except Exception as e:
        print(f"Error executing command: {e}")
