import time
from screenUpdater import buffer
import inputManager as input


class actions:
    def __init__(self):
        self.gameOn = True

    def newGame(self, activate):
        if activate:
            self.gameOn = False
        return str("New Game")

    def loadGame(self, activate):
        if activate:
            self.gameOn = False
        return str("Load Save")

    def quitGame(self, activate):
        if activate:
            self.gameOn = False
        return str("Quit")

    def select(self):
        gui.activate = True


gui = buffer(64, 24)
gui.setScene("Main Menu")
gui.setStats("")
gui.setTimerLength(5)

actions = actions()

welcomePage = ["jee", "juu"]
question = ["Main Menu", [actions.newGame, actions.loadGame, actions.quitGame]]

gui.setContent(welcomePage)
gui.setQuestion(question)

input = input.inputManager()

gui.updateFrame()

fps = 12


def getInput():
    char = input.getChar()
    if char != "":
        if char == "s":
            gui.selection += 1
        elif char == "w":
            gui.selection -= 1
        elif char == " ":
            actions.select()


frameStartTime = None
secondStartTime = None
while actions.gameOn:
    if frameStartTime is None:
        frameStartTime = time.time()
    if secondStartTime is None:
        secondStartTime = time.time()

    elapsedFrameTime = time.time() - frameStartTime
    elapsedSecondTime = time.time() - secondStartTime
    getInput()
    if elapsedSecondTime >= 1:
        gui.setTimerSeconds(2)
    if elapsedFrameTime >= (1 / fps):
        gui.updateFrame()
        frameStartTime = None
