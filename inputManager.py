import sys
import tty
import termios
import select


class inputManager:
    def __init__(self):
        self.previousKey = ""
        self.previousKeys = []
        self.maxKeyLenght = 5

    def getChar(self):
        fd = sys.stdin.fileno()
        oldSettings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            # Check if there's input available within a short timeout
            if select.select([sys.stdin], [], [], 0.005)[0]:
                char = sys.stdin.read(1)
                self.previousKey = char

                self.previousInputs(char)
                return char
            else:
                return ""
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)

    def getText(self):
        return self.previousKeys

    def previousInputs(self, newChar):
        self.previousKeys.append(newChar)
        if len(self.previousKeys) >= self.maxKeyLenght:
            self.previousKeys.pop(0)
