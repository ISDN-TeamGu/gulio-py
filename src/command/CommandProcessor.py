class CommandProcessor:
    def __init__(self):
        self.processRate = 1.0
    
    def run_command(self, commandLine):
        # Split the command line into command and arguments
        command_tokens = commandLine.split()
        command = command_tokens[0]
        arguments = command_tokens[1:]
        
        # Check the command and perform the corresponding action
        if command == "playMusic":
            self.play_music(arguments)
        elif command == "setRate":
            self.set_rate(arguments)
        elif command == "quit":
            self.quit()
        else:
            print("Unknown command:", command)
    
    def play_music(self, arguments):
        # Handle the playMusic command with its arguments
        if len(arguments) == 0:
            print("Playing music...")
        else:
            song_name = arguments[0]
            print("Playing music:", song_name)
    
    def set_rate(self, arguments):
        # Handle the setRate command with its arguments
        if len(arguments) == 0:
            print("Please provide a rate value.")
        else:
            rate = float(arguments[0])
            self.processRate = rate
            print("Process rate set to:", rate)
    
    def quit(self):
        # Handle the quit command
        print("Quitting...")
        # Add your code here to perform any necessary cleanup or termination actions