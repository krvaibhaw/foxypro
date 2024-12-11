import os
import json
import platform
import subprocess

# Path where aliases are saved between sessions
ALIAS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "aliases.json")

# ── Colour codes ────────────────────────────────────────────────────────────

class Colors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKCYAN    = '\033[96m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

# ── Mutable shell state ──────────────────────────────────────────────────────

command_history: list[str] = []

aliases: dict[str, str] = {
    'l':   'ls',
    'll':  'ls -la',
    'cls': 'clear',
    'p':   'pwd',
    'h':   'history',
    'mk':  'mkdir',
    'rm':  'rmdir',
}

# ── Alias persistence ────────────────────────────────────────────────────────

def load_aliases() -> None:
    """Load saved aliases from disk and merge into the aliases dict."""
    if not os.path.exists(ALIAS_FILE):
        return
    try:
        with open(ALIAS_FILE, 'r') as f:
            saved = json.load(f)
        if isinstance(saved, dict):
            aliases.update(saved)
    except Exception as e:
        print(f"{Colors.WARNING}⚠ Could not load aliases: {e}{Colors.ENDC}")


def save_aliases() -> None:
    """Save the current aliases dict to disk."""
    try:
        with open(ALIAS_FILE, 'w') as f:
            json.dump(aliases, f, indent=2)
    except Exception as e:
        print(f"{Colors.WARNING}⚠ Could not save aliases: {e}{Colors.ENDC}")

# ── Built-in command names (aliases are also considered built-ins)
BUILTINS = [
    'cd', 'pwd', 'echo', 'clear', 'help',
    'dir', 'ls', 'set', 'history',
    'mkdir', 'rmdir', 'type', 'alias', 'unalias', 'env',
]


# ── History helpers ──────────────────────────────────────────────────────────

def add_to_history(command: str) -> None:
    """Append a non-empty command to the history list."""
    if command.strip():
        command_history.append(command.strip())

# ── Dispatch helpers ─────────────────────────────────────────────────────────

def is_builtin(command: str) -> bool:
    """Return True when the first word of *command* is a built-in or alias."""
    cmd_name = command.split()[0] if command.split() else ""
    return cmd_name in BUILTINS or cmd_name in aliases


def execute_builtin(command: str) -> None:
    """Parse and execute a built-in command."""
    parts    = command.split(maxsplit=1)
    cmd_name = parts[0]
    args     = parts[1] if len(parts) > 1 else ""

    # Resolve alias first (recursive so alias chains work)
    if cmd_name in aliases:
        full_command = aliases[cmd_name] + (" " + args if args else "")
        execute_builtin(full_command)
        return

    dispatch = {
        "cd":      lambda: builtin_cd(args),
        "pwd":     lambda: builtin_pwd(),
        "echo":    lambda: builtin_echo(args),
        "clear":   lambda: builtin_clear(),
        "help":    lambda: builtin_help(),
        "dir":     lambda: builtin_ls(args),
        "ls":      lambda: builtin_ls(args),
        "set":     lambda: builtin_set(args),
        "history": lambda: builtin_history(),
        "mkdir":   lambda: builtin_mkdir(args),
        "rmdir":   lambda: builtin_rmdir(args),
        "type":    lambda: builtin_type(args),
        "alias":   lambda: builtin_alias(args),
        "unalias": lambda: builtin_unalias(args),
        "env":     lambda: builtin_env(args),
    }

    handler = dispatch.get(cmd_name)
    if handler:
        handler()
    else:
        print(f"Unknown built-in command: {cmd_name}")
