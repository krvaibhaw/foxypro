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
