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
