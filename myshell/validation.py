import re


class Colors:
    FAIL = '\033[91m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
def validate_command(command):
    """Validate command syntax before execution."""
    if not command.strip():
        return False, "Empty command"

    # Count quotes, ignoring escaped ones
    double_quotes = command.count('"') - command.count('\\"')
    single_quotes = command.count("'") - command.count("\\'")

    if double_quotes % 2 != 0:
        return False, "Mismatched double quotes"

    if single_quotes % 2 != 0:
        return False, "Mismatched single quotes"

    # Reject invalid pipe-redirect combo
    if '|>' in command:
        return False, "Invalid operator: |> (did you mean | or > ?)"

    # Reject empty pipe segments like:  cmd |  | cmd
    if '|' in command:
        pipe_parts = command.split('|')
        for part in pipe_parts:
            if not part.strip():
                return False, "Pipe operator has an empty command segment"

    # Reject dangling redirection operators with no filename
    # e.g. "echo hi >" or "echo hi >>"
    stripped = command.strip()
    if re.search(r'>>\s*$', stripped) or re.search(r'(?<!>)>\s*$', stripped):
        return False, "Redirection operator has no target filename"

    if re.search(r'<\s*$', stripped):
        return False, "Input redirection has no source filename"

    return True, "Valid"
