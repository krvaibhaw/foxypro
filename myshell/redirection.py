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


def handle_append_redirect(command):
    """Handle output redirection: cmd >> file  (append)"""
    try:
        parts = command.split('>>', 1)
        cmd = parts[0].strip()
        filename = parts[1].strip()
        if not filename:
            print("Error: No filename specified for '>>'")
            return
        with open(filename, 'a') as f:
            subprocess.run(cmd, stdout=f, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
    except Exception as e:
        print(f"Error: {e}")


def handle_input_redirect(command):
    """Handle input redirection: cmd < file"""
    try:
        parts = command.split('<', 1)
        cmd = parts[0].strip()
        filename = parts[1].strip()
        if not filename:
            print("Error: No filename specified for '<'")
            return
        with open(filename, 'r') as f:
            subprocess.run(cmd, stdin=f, check=True, shell=True)
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
    except Exception as e:
        print(f"Error: {e}")


def handle_pipe(command):
    """
    Handle piped commands: cmd1 | cmd2 | cmd3 ...
    Chains processes so stdout of each feeds stdin of the next.
    """
    try:
        pipe_parts = [p.strip() for p in command.split('|')]
        if len(pipe_parts) < 2:
            run_simple(command)
            return

        processes = []
        prev_stdout = None

        for i, part in enumerate(pipe_parts):
            is_last = (i == len(pipe_parts) - 1)
            stdin_pipe = prev_stdout
            stdout_pipe = None if is_last else subprocess.PIPE

            proc = subprocess.Popen(
                part,
                shell=True,
                stdin=stdin_pipe,
                stdout=stdout_pipe,
            )
            # Close the previous process's stdout in the parent so the pipe
            # delivers EOF to the next process when it finishes.
            if prev_stdout is not None:
                prev_stdout.close()

            prev_stdout = proc.stdout
            processes.append(proc)

        # Wait for all processes to complete
        for proc in processes:
            proc.wait()

    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
    except Exception as e:
        print(f"Error: {e}")
