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