import subprocess
import shlex

ef handle_redirection(command):
    parts = shlex.split(command)
    if '>' in parts:
        index = parts.index('>')
        filename = parts[index + 1]
        parts = parts[:index]
        with open(filename, 'w') as f:
            subprocess.run(parts, stdout=f)
    lif '>>' in parts:
        index = parts.index('>>')
        filename = parts[index + 1]
        parts = parts[:index]
        with open(filename, 'a') as f:
            subprocess.run(parts, stdout=f)
