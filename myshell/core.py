def main_loop():
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
