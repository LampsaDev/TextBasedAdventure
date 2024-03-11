import sys
import select


class inputManager:
    def __init__(self):
        self.previousKey = ""

    def getPrevious(self):
        return self.previousKey

    def getKeypress(self, timeout=1 / 24):
        # Wait for input with a timeout
        ready, _, _ = select.select([sys.stdin], [], [], timeout)
        if ready:
            print(sys.stdin)
            # If input is available, read a single character
            key = sys.stdin.read(1)
            self.previousKey = key
            return key + "\n"
        else:
            # If no input is available within the timeout period, return None
            return None

    def getText(self):
        # Read input from the command line
        userInput = input("> ")
        return userInput
