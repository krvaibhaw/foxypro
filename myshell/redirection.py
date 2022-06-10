import subprocess
import shlex
def handle_redirection(command):
    parts = shlex.split(command)
    try:
        if '>' in parts:
            index = parts.index('>')
            filename = parts[index + 1]
            parts = parts[:index]
            with open(filename, 'w') as f:
                subprocess.run(parts, stdout=f, check=True)
        elif '>>' in parts:
            index = parts.index('>>')
            filename = parts[index + 1]
            parts = parts[:index]
            with open(filename, 'a') as f:
                subprocess.run(parts, stdout=f, check=True)
        elif '<' in parts:
            index = parts.index('<')
            filename = parts[index + 1]
            parts = parts[:index]
            with open(filename, 'r') as f:
                subprocess.run(parts, stdin=f, check=True)
        else:
            subprocess.run(parts, check=True)
    except subprocess.CalledProcessError:
        print(f"Command failed: {' '.join(parts)}")
    except FileNotFoundError:
        print(f"Command not found: {' '.join(parts)}")
    except Exception as e:
        print(f"Error executing command '{' '.join(parts)}': {e}")
