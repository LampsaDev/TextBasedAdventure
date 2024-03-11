import sys
import tty
import termios
import select


class inputManager:
    def __init__(self):
        self.previousKey = ""

    def getChar(self):
        fd = sys.stdin.fileno()
        oldSettings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            # Check if there's input available within a short timeout
            if select.select([sys.stdin], [], [], 0.01)[0]:
                char = sys.stdin.read(1)
                return char
            else:
                return ""
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)
