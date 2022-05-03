def parse_command(command):
    background = command.strip().endswith('&')
    if background:
        command = command[:-1].strip()
    return background, command
