def parse_command(command):
    """Parse command for background execution (&) flag."""
    background = command.strip().endswith('&')
    if background:
        command = command[:-1].strip()
    return background, command
