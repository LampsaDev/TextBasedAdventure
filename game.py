import time
from screenUpdater import buffer
import inputManager as input
import optionHandler
import os


gui = buffer(64, 24)
gui.setScene("Main Menu")
gui.setStats("")
gui.setTimerLength(10)

gameLogic = optionHandler.Generic(gui)

welcomePage = ["jee", "juu"]
question = gameLogic.currentView.getGuiFormat()

gui.setContent(welcomePage)
gui.setQuestion(question)

input = input.inputManager()

gui.updateFrame()

gui.setTimerLength(0)


def getInput():
    char = input.getChar()
    gameLogic.checkInput(char)


frameStartTime = None
secondStartTime = None
while gameLogic.getGameStatus():
    if frameStartTime is None:
        frameStartTime = time.time()
    if secondStartTime is None:
        secondStartTime = time.time()

    elapsedFrameTime = time.time() - frameStartTime
    elapsedSecondTime = time.time() - secondStartTime
    getInput()
    if elapsedSecondTime >= 1:
        gameLogic.secondPassed()
        secondStartTime = None
    if elapsedFrameTime >= (1 / gameLogic.getFPS()):
        gui.updateFrame()
        frameStartTime = None

os.system("clear")
