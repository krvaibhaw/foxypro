from myshell.redirection import handle_redirection
from myshell.background import handle_background
from myshell.utils import parse_command

def main_loop():
    print("\n")
    print(" ********                                                  ");
    print("/**/////                    **   ** ******                 ");
    print("/**        ******  **   ** //** ** /**///** ******  ****** ");
    print("/*******  **////**//** **   //***  /**  /**//**//* **////**");
    print("/**////  /**   /** //***     /**   /******  /** / /**   /**");
    print("/**      /**   /**  **/**    **    /**///   /**   /**   /**");
    print("/**      //******  ** //**  **     /**     /***   //****** ");
    print("//        //////  //   //  //      //      ///     //////  ");
    print("\n")
    print("////////////////////////////////////////////////////////////");
    print("************************************************************");
    print("\n")
    print("Welcome to Foxypro Shell :)\n")

    while True:        
        user_input = input("$ ")
        if user_input == "exit":
            break
        process_command(user_input)

def process_command(command):
    
    background, command = parse_command(command)
    if background:
        handle_background(command)
    else:
        handle_redirection(command)
        
