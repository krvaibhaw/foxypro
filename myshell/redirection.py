import subprocess
import platform


def handle_redirection(command):
    """
    Dispatch command to the correct handler based on redirection/pipe operators.
    Order matters: '>>' must be checked before '>' to avoid incorrect splitting.
    """
    if '|' in command:
        handle_pipe(command)
    elif '>>' in command:
        handle_append_redirect(command)
    elif '>' in command:
        handle_write_redirect(command)
    elif '<' in command:
        handle_input_redirect(command)
    else:
        run_simple(command)

def run_simple(command):
    """Run a plain command with no redirection."""
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
    except FileNotFoundError:
        print(f"Command not found: {command.split()[0]}")
    except Exception as e:
        print(f"Error: {e}")

def handle_write_redirect(command):
    """Handle output redirection: cmd > file  (overwrite)"""
    try:
        parts = command.split('>', 1)
        cmd = parts[0].strip()
        filename = parts[1].strip()
        if not filename:
            print("Error: No filename specified for '>'")
            return
        with open(filename, 'w') as f:
            subprocess.run(cmd, stdout=f, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
    except Exception as e:
        print(f"Error: {e}")
