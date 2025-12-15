# 🦊 Foxypro Shell

A lightweight, cross-platform interactive shell built entirely in Python with zero external dependencies. Foxypro provides a familiar terminal experience with built-in commands, piping, redirection, background processes, environment variables, command chaining, and persistent aliases — all implemented from scratch using only the Python standard library.

---


## Features

| Feature | Details |
|---|---|
| Built-in commands | `cd`, `pwd`, `ls`, `dir`, `mkdir`, `rmdir`, `echo`, `type`, `clear`, `set`, `env`, `history`, `alias`, `unalias`, `help`, `exit` |
| Piping | Multi-stage pipes with proper `stdout → stdin` chaining via `subprocess.Popen` |
| Output redirection | Write (`>`) and append (`>>`) to files |
| Input redirection | Feed a file as stdin (`<`) |
| Background execution | Run any command in the background with `&` |
| Command chaining | Run multiple commands sequentially with `;`, quote-aware splitting |
| Variable expansion | `$VAR` and `${VAR}` syntax, expands before execution |
| Persistent aliases | Saved to `myshell/aliases.json`, restored automatically on startup |
| Command validation | Pre-execution checks for mismatched quotes, empty pipe segments, dangling operators |
| Colored output | ANSI color codes for prompts, errors, success messages, and command output |
| Cross-platform | Works on Windows, macOS, and Linux |
| Zero dependencies | Standard library only: `os`, `re`, `json`, `subprocess`, `platform` |

---

## Project Structure

```
foxypro/
├── bin/
│   └── main.py              # Entry point — run this file to start the shell
└── myshell/
    ├── __init__.py          # Python package marker
    ├── aliases.json         # Auto-generated on first alias save; persists aliases
    ├── background.py        # Handles background process execution (&)
    ├── builtins.py          # All built-in command implementations + alias persistence
    ├── core.py              # Main loop, command processing pipeline, variable expansion
    ├── redirection.py       # Piping, output redirection, input redirection
    ├── utils.py             # parse_command() — strips & flag, returns (background, cmd)
    └── validation.py        # Pre-execution syntax validation
```

### What each file does

**`bin/main.py`** — The only file you run directly. Adds the project root to `sys.path` and calls `main_loop()` from `core.py`.

**`myshell/core.py`** — The brain of the shell. Contains the `main_loop()` REPL, the command processing pipeline (`process_command` → `process_single_command`), variable expansion via regex, and quote-aware semicolon splitting. Imports from every other module and orchestrates the full execution flow.

**`myshell/builtins.py`** — Implements every built-in command as a standalone function (`builtin_cd`, `builtin_echo`, `builtin_alias`, etc.). Also owns the `aliases` dict (the live in-memory alias table), `command_history` list, and the `load_aliases()` / `save_aliases()` persistence functions.

**`myshell/redirection.py`** — Handles everything involving `|`, `>`, `>>`, and `<`. Uses `subprocess.Popen` chains for multi-stage pipes so stdout of each process is correctly wired to stdin of the next. Checks `>>` before `>` to avoid the common operator-matching bug.

**`myshell/background.py`** — Launches a command with `subprocess.Popen` (no `wait()`) and immediately prints the PID, returning control to the shell.

**`myshell/validation.py`** — Runs before any command executes. Checks for mismatched quotes, the invalid `|>` operator, empty pipe segments, and dangling redirection operators with no filename.

**`myshell/utils.py`** — Single function `parse_command()` that detects a trailing `&` and returns `(True, command_without_ampersand)` or `(False, command)`.

**`myshell/aliases.json`** — Plain JSON file, auto-created on the first `alias` or `unalias` call. Merge-loaded on startup so default aliases are always present even if the file predates them.

---

## Architecture Overview

```
bin/main.py
    └── core.main_loop()
            │
            ├── load_aliases()              ← restore from aliases.json on startup
            │
            └── REPL loop
                    │
                    ├── input(f"{cwd}$ ")
                    │
                    └── process_command(user_input)
                            │
                            ├── 1. validate_command()     ← syntax check
                            ├── 2. expand_variables()     ← $VAR substitution
                            ├── 3. add_to_history()       ← record command
                            ├── 4. _split_on_semicolons() ← handle ; chaining
                            │
                            └── process_single_command()