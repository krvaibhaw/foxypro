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
