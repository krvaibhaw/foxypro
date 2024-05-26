import os
import re

from myshell.redirection import handle_redirection
from myshell.background import handle_background
from myshell.utils import parse_command
from myshell.builtins import execute_builtin, is_builtin, add_to_history, load_aliases, save_aliases
from myshell.validation import validate_command, print_error

BANNER = r"""
 ********                                                  
/**/////                    **   ** ******                 
/**        ******  **   ** //** ** /**///** ******  ****** 
/*******  **////**//** **   //***  /**  /**//**//* **////**
/**////  /**   /** //***     /**   /******  /** / /**   /**
/**      /**   /**  **/**    **    /**///   /**   /**   /**
/**      //******  ** //**  **     /**     /***   //****** 
//        //////  //   //  //      //      ///     //////  
"""

def main_loop():
    print(BANNER)
    print("=" * 60)
    print("  Welcome to Foxypro Shell  |  type 'help' to get started")
    print("=" * 60 + "\n")

    load_aliases()  # restore aliases saved from previous sessions

    while True:
        try:
            cwd = os.getcwd()
            user_input = input(f"{cwd}$ ")

            if user_input.strip() == "exit":
                save_aliases()
                print("Goodbye!")
                break

            if user_input.strip():
                process_command(user_input)

        except KeyboardInterrupt:
            # Ctrl-C cancels the current line; don't exit
            print()

        except EOFError:
            save_aliases()
            print("\nGoodbye!")
            break

        except Exception as e:
            print(f"Unexpected error: {e}")

def expand_variables(command: str) -> str:
    """Expand $VAR and ${VAR} style environment variables in a command."""
    def replace_var(match):
        var_name = match.group(1) or match.group(2)
        return os.environ.get(var_name, "")

    return re.sub(r'\$\{(\w+)\}|\$(\w+)', replace_var, command)

def process_command(command: str) -> None:
    """
    Top-level command processor.
    Handles: validation → variable expansion → history → chaining → dispatch.
    """
    # 1. Validate
    is_valid, message = validate_command(command)
    if not is_valid:
        print_error(f"Syntax error: {message}")
        return
    
    # 2. Expand environment variables
    command = expand_variables(command)

    # 3. Record in history (store the expanded form)
    add_to_history(command)

    # 4. Handle command chaining with ';'
    #    Only split on ';' when there is no pipe in the whole command string,
    #    to keep "cmd1 | cmd2 ; cmd3" handled correctly.
    if ';' in command:
        # Respect semicolons even when a pipe is present by processing
        # each semicolon-delimited segment independently.
        commands = _split_on_semicolons(command)
        for cmd in commands:
            cmd = cmd.strip()
            if cmd:
                process_single_command(cmd)
        return

    process_single_command(command)

def _split_on_semicolons(command: str) -> list[str]:
    """
    Split on ';' while ignoring semicolons inside quoted strings.
    """
    parts = []
    current = []
    in_single = False
    in_double = False

    for ch in command:
        if ch == "'" and not in_double:
            in_single = not in_single
            current.append(ch)
        elif ch == '"' and not in_single:
            in_double = not in_double
            current.append(ch)
        elif ch == ';' and not in_single and not in_double:
            parts.append(''.join(current))
            current = []
        else:
            current.append(ch)

    if current:
        parts.append(''.join(current))

    return parts
