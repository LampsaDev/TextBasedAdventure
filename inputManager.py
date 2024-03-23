import sys
import tty
import termios
import select
import os


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
            if select.select([sys.stdin], [], [], 0.05)[0]:
                char = sys.stdin.read(1)
                self.previousKey = char

                self.previousInputs(char)
                return char
            else:
                return ""
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)

    def getText(self, maxLen=15, title="Input", gui=None):
        text = []
        while True:
            self.getChar()
            line = "".join(text)
            lineLen = str(len(line)) + "/" + str(maxLen)
            os.system("clear")
            if gui:
                gui.drawTextBox([title + " " + lineLen, line])
            else:
                print(title)
                print(line)
                print(lineLen)

            if self.previousKey == "\r":
                return "".join(text)
            elif self.previousKey == "\x7f" and len(text) > 0:
                text.pop()
            elif self.previousKey != "" and len(text) < maxLen:
                text.append(self.previousKey)
            self.previousKey = ""

    def previousInputs(self, newChar):
        self.previousKeys.append(newChar)
        if len(self.previousKeys) >= self.maxKeyLenght:
            self.previousKeys.pop(0)
