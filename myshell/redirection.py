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
