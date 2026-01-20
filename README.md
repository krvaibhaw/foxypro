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
                                    │
                                    ├── parse_command()       ← detect & flag
                                    │
                                    ├── is_builtin() && no operators
                                    │       └── execute_builtin()
                                    │
                                    ├── background == True
                                    │       └── handle_background()
                                    │
                                    └── else
                                            └── handle_redirection()
                                                    ├── handle_pipe()
                                                    ├── handle_write_redirect()
                                                    ├── handle_append_redirect()
                                                    ├── handle_input_redirect()
                                                    └── run_simple()
```

## Requirements

- Python **3.10 or higher** (uses `list[str]` type hints which require 3.9+, and `match` style patterns internally)
- No pip installs, no virtual environment needed
- Works on Windows 10/11, macOS 10.15+, Ubuntu 20.04+

Verify your Python version:

```bash
python --version
# or
python3 --version
```

---

## Installation

**Option 1 — Clone with git:**

```bash
git clone https://github.com/yourname/foxypro.git
cd foxypro
```

**Option 2 — Download ZIP:**

Download and extract the project folder, then open a terminal inside the `foxypro/` directory.

No `pip install` step is required.

---

## Getting Started

Start the shell from inside the `foxypro/` directory:

```bash
python bin/main.py
```

You will see the ASCII banner followed by the shell prompt:

```
 ********
/**/////                    **   ** ******
/**        ******  **   ** //** ** /**///**  ******  ******
/*******  **////**//** **   //***  /**  /**//**//* **////**
/**////  /**   /** //***     /**   /******  /** / /**   /**
/**      /**   /**  **/**    **    /**///   /**   /**   /**
/**      //******  ** //**  **     /**     /***   //******
//        //////  //   //  //      //      ///     //////

============================================================
  Welcome to Foxypro Shell  |  type 'help' to get started
============================================================

/home/yourname$
```

The prompt always shows your **current working directory** followed by `$`.

Type `help` to see the full command reference, or `exit` to quit.

---

## How a Command Gets Executed

Understanding the execution pipeline helps when debugging unexpected behaviour.

**1. Validation** (`validation.py`)
The raw input is checked for syntax errors before anything runs. If validation fails, an error is printed and execution stops — the command never reaches the shell or OS.

**2. Variable expansion** (`core.py → expand_variables`)
All `$VAR` and `${VAR}` tokens are replaced with their current values from `os.environ`. If a variable is not set, it expands to an empty string. Expansion happens on the whole command string before splitting.

**3. History recording** (`builtins.py → add_to_history`)
The expanded command is appended to the in-memory `command_history` list.

**4. Semicolon splitting** (`core.py → _split_on_semicolons`)
If the command contains `;`, it is split into individual sub-commands. The splitter is quote-aware — a `;` inside `"..."` or `'...'` is not treated as a separator. Each sub-command is then processed independently through steps 5–7.

**5. Background flag detection** (`utils.py → parse_command`)
If the command ends with `&`, `background=True` is returned and the `&` is stripped from the command string.

**6. Routing decision** (`core.py → process_single_command`)
Three possible routes:
- **Built-in, no operators** → `execute_builtin()` in `builtins.py`
- **Background** → `handle_background()` in `background.py`
- **Everything else** (external commands, redirection, pipes) → `handle_redirection()` in `redirection.py`

> **Why built-ins with operators go to `handle_redirection`:** A command like `echo hello >> file.txt` starts with `echo` which is a built-in — but it has a `>>` operator. If it were routed to `execute_builtin`, it would print `hello >> file.txt` literally. The check `is_builtin() and not _has_redirection_or_pipe()` ensures that any built-in command containing an operator is passed to the system shell via `handle_redirection`, which handles the operator correctly.

**7. Execution**
- `handle_background` — calls `subprocess.Popen` without waiting, prints the PID
- `handle_redirection` — dispatches to the correct handler (`>>` checked before `>` to avoid substring matching bugs), uses `subprocess.Popen` chains for pipes
- `execute_builtin` — calls the matching `builtin_*` function directly in Python

---