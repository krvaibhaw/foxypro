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

# ── Built-in implementations ─────────────────────────────────────────────────

def builtin_cd(args: str) -> None:
    """Change the current working directory."""
    path = args.strip() if args else os.path.expanduser("~")
    try:
        os.chdir(path)
        print(f"Changed to {os.getcwd()}")
    except FileNotFoundError:
        print(f"{Colors.FAIL}✗ cd: directory not found: {path}{Colors.ENDC}")
    except NotADirectoryError:
        print(f"{Colors.FAIL}✗ cd: not a directory: {path}{Colors.ENDC}")
    except PermissionError:
        print(f"{Colors.FAIL}✗ cd: permission denied: {path}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}✗ cd: {e}{Colors.ENDC}")


def builtin_pwd() -> None:
    """Print the current working directory."""
    print(f"{Colors.OKBLUE}{os.getcwd()}{Colors.ENDC}")

def builtin_echo(args: str) -> None:
    """Print text to stdout."""
    print(args)


def builtin_clear() -> None:
    """Clear the terminal screen."""
    os.system("cls" if platform.system() == "Windows" else "clear")


def builtin_help() -> None:
    """Display help information."""
    C = Colors
    help_text = f"""
{C.BOLD}{C.OKBLUE}╔══════════════════════════════════════════════════════╗{C.ENDC}
{C.BOLD}{C.OKBLUE}║          Foxypro Shell - Built-in Commands           ║{C.ENDC}
{C.BOLD}{C.OKBLUE}╚══════════════════════════════════════════════════════╝{C.ENDC}

{C.OKGREEN}{C.BOLD}Navigation:{C.ENDC}
  {C.OKCYAN}cd{C.ENDC} [path]              Change directory (home if no path given)
  {C.OKCYAN}pwd{C.ENDC}                    Print current working directory

{C.OKGREEN}{C.BOLD}File Operations:{C.ENDC}
  {C.OKCYAN}ls{C.ENDC} / {C.OKCYAN}dir{C.ENDC} [path]       List directory contents
  {C.OKCYAN}mkdir{C.ENDC} <dir>            Create a directory
  {C.OKCYAN}rmdir{C.ENDC} <dir>            Remove an empty directory
  {C.OKCYAN}type{C.ENDC} <file>            Display file contents
  {C.OKCYAN}echo{C.ENDC} [text]            Print text to stdout

{C.OKGREEN}{C.BOLD}System:{C.ENDC}
  {C.OKCYAN}clear{C.ENDC}                  Clear the screen
  {C.OKCYAN}set{C.ENDC} VAR=value         Set an environment variable
  {C.OKCYAN}env{C.ENDC} [VAR]             Show all (or one) environment variable(s)
  {C.OKCYAN}history{C.ENDC}               Show command history
  {C.OKCYAN}alias{C.ENDC} [name cmd]      Create/list aliases
  {C.OKCYAN}unalias{C.ENDC} <name>        Remove an alias
  {C.OKCYAN}help{C.ENDC}                  Show this help message
  {C.OKCYAN}exit{C.ENDC}                  Exit the shell

{C.OKGREEN}{C.BOLD}Operators:{C.ENDC}
  {C.WARNING}|{C.ENDC}   pipe        Pipe output of one command to another
  {C.WARNING}>{C.ENDC}   redirect    Write stdout to a file (overwrite)
  {C.WARNING}>>{C.ENDC}  append      Append stdout to a file
  {C.WARNING}<{C.ENDC}   input       Read stdin from a file
  {C.WARNING}&{C.ENDC}   background  Run command in the background
  {C.WARNING};{C.ENDC}   chain       Run multiple commands sequentially
  {C.WARNING}$VAR{C.ENDC}            Expand an environment variable

{C.OKGREEN}{C.BOLD}Examples:{C.ENDC}
  $ echo Hello > file.txt          Write to file
  $ cat file.txt >> log.txt        Append to file
  $ ls | grep .py                  Pipe output through filter
  $ cd /tmp                        Change directory
  $ set MYVAR=hello                Set a variable
  $ echo $MYVAR                    Expand a variable
  $ sleep 5 &                      Run in background
  $ echo a; echo b; echo c         Chain commands
  $ alias ll ls -la                Create alias
"""
    print(help_text)

def builtin_ls(args: str) -> None:
    """List directory contents (cross-platform)."""
    is_windows = platform.system() == "Windows"
    cmd = ("dir " if is_windows else "ls ") + args if args else ("dir" if is_windows else "ls")
    try:
        subprocess.run(cmd, shell=True)
    except Exception as e:
        print(f"{Colors.FAIL}✗ Error listing directory: {e}{Colors.ENDC}")

def builtin_set(args: str) -> None:
    """Set an environment variable: set VAR=value"""
    if not args or "=" not in args:
        print(f"{Colors.FAIL}✗ Usage: set VAR=value{Colors.ENDC}")
        return
    var_name, var_value = args.split("=", 1)
    var_name  = var_name.strip()
    var_value = var_value.strip()
    if not var_name:
        print(f"{Colors.FAIL}✗ Variable name cannot be empty{Colors.ENDC}")
        return
    try:
        os.environ[var_name] = var_value
        print(f"{Colors.OKGREEN}✓ Set {var_name}={var_value}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}✗ Error setting variable: {e}{Colors.ENDC}")

def builtin_history() -> None:
    """Display command history."""
    if not command_history:
        print(f"{Colors.WARNING}No command history yet{Colors.ENDC}")
        return
    print(f"\n{Colors.BOLD}{Colors.OKBLUE}Command History:{Colors.ENDC}")
    print("-" * 60)
    for i, cmd in enumerate(command_history, 1):
        print(f"{Colors.OKCYAN}{i:4d}{Colors.ENDC}  {cmd}")
    print("-" * 60)

def builtin_mkdir(args: str) -> None:
    """Create a directory."""
    if not args:
        print(f"{Colors.FAIL}✗ Usage: mkdir <dirname>{Colors.ENDC}")
        return
    path = args.strip()
    try:
        os.mkdir(path)
        print(f"{Colors.OKGREEN}✓ Created directory: {path}{Colors.ENDC}")
    except FileExistsError:
        print(f"{Colors.FAIL}✗ Directory already exists: {path}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}✗ Error: {e}{Colors.ENDC}")

def builtin_rmdir(args: str) -> None:
    """Remove an empty directory."""
    if not args:
        print(f"{Colors.FAIL}✗ Usage: rmdir <dirname>{Colors.ENDC}")
        return
    path = args.strip()
    try:
        os.rmdir(path)
        print(f"{Colors.OKGREEN}✓ Removed directory: {path}{Colors.ENDC}")
    except FileNotFoundError:
        print(f"{Colors.FAIL}✗ Directory not found: {path}{Colors.ENDC}")
    except OSError:
        print(f"{Colors.FAIL}✗ Directory not empty or cannot be removed: {path}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}✗ Error: {e}{Colors.ENDC}")


def builtin_type(args: str) -> None:
    """Display the contents of a file."""
    if not args:
        print(f"{Colors.FAIL}✗ Usage: type <filename>{Colors.ENDC}")
        return
    filepath = args.strip()
    try:
        with open(filepath, 'r') as f:
            print(f.read(), end="")
    except FileNotFoundError:
        print(f"{Colors.FAIL}✗ File not found: {filepath}{Colors.ENDC}")
    except IsADirectoryError:
        print(f"{Colors.FAIL}✗ Is a directory: {filepath}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}✗ Error: {e}{Colors.ENDC}")

def builtin_alias(args: str) -> None:
    """Create or display aliases."""
    if not args:
        if not aliases:
            print(f"{Colors.WARNING}No aliases defined{Colors.ENDC}")
            return
        print(f"\n{Colors.BOLD}{Colors.OKBLUE}Aliases:{Colors.ENDC}")
        print("-" * 40)
        for name, cmd in sorted(aliases.items()):
            print(f"  {Colors.OKCYAN}{name:12}{Colors.ENDC}-> {cmd}")
        print("-" * 40)
    else:
        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            # Show a single alias if it exists
            if parts[0] in aliases:
                print(f"  {Colors.OKCYAN}{parts[0]:12}{Colors.ENDC}-> {aliases[parts[0]]}")
            else:
                print(f"{Colors.FAIL}✗ Usage: alias <name> <command>{Colors.ENDC}")
            return
        alias_name, alias_cmd = parts[0], parts[1]
        aliases[alias_name] = alias_cmd
        save_aliases()
        print(f"{Colors.OKGREEN}✓ Alias created: {alias_name} -> {alias_cmd}{Colors.ENDC}")

def builtin_unalias(args: str) -> None:
    """Remove a defined alias."""
    if not args:
        print(f"{Colors.FAIL}✗ Usage: unalias <name>{Colors.ENDC}")
        return
    alias_name = args.strip()
    if alias_name in aliases:
        del aliases[alias_name]
        save_aliases()
        print(f"{Colors.OKGREEN}✓ Alias removed: {alias_name}{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}✗ Alias not found: {alias_name}{Colors.ENDC}")